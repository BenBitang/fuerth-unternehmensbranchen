#!/usr/bin/env python3
"""
Advanced Playwright web scraper with intelligent page detection
This version is more robust and handles various page structures
"""

import csv
import asyncio
from typing import List, Tuple, Optional, Dict
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import json
from datetime import datetime


class FurthCompanyScraperAdvanced:
    """Advanced scraper with better error handling and page detection"""
    
    def __init__(self, headless: bool = True, debug: bool = False):
        """
        Initialize the scraper
        
        Args:
            headless: Run browser in headless mode
            debug: Enable debug output
        """
        self.url = "https://service-on.fuerth.de/KWISwebComp/sections/search/company.jsf"
        self.companies = []
        self.headless = headless
        self.debug = debug
        
    def _log(self, message: str):
        """Log message if debug is enabled"""
        if self.debug:
            print(f"[DEBUG] {message}")
        else:
            print(message)
        
    async def scrape(self) -> List[Tuple[str, str]]:
        """Main scraping method - returns (name, branch)"""
        self._log("Starting Playwright browser...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            try:
                companies = await self._scrape_all_branches(page)
            except Exception as e:
                print(f"Error during scraping: {e}")
                companies = []
            finally:
                await context.close()
                await browser.close()
                
            return companies
            
    async def _scrape_all_branches(self, page: Page) -> List[Tuple[str, str]]:
        """Scrape companies by going through all branches"""
        print("Navigating to search page...")
        await page.goto(self.url, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(2000)
        
        all_companies = []
        
        # Get all main branches
        print("\n=== Extracting main branches ===")
        branches = await self._get_all_branches(page)
        print(f"Found {len(branches)} main branches")
        
        # Go through each branch
        for branch_idx, (branch_value, branch_name) in enumerate(branches, 1):
            print(f"\n{'='*60}")
            print(f"[{branch_idx}/{len(branches)}] Processing branch: {branch_name}")
            print(f"{'='*60}")
            
            # Navigate back to search form to ensure clean state
            if branch_idx > 1:
                print(f"  Navigating back to search form...")
                await page.goto(self.url, wait_until='domcontentloaded', timeout=30000)
                await page.wait_for_timeout(1000)
            
            # Reset search first (clear previous results)
            reset_button = await page.query_selector('button[id*="resetButton"]')
            if reset_button:
                await reset_button.click()
                await page.wait_for_timeout(1000)
            
            # Select this branch (includes waiting for AJAX)
            await self._select_branch(page, branch_value)
            
            # Note: Sub-branch filtering doesn't work with PrimeFaces dropdowns in Playwright
            # So we'll search all companies in this branch without sub-branch filter
            print(f"  Searching all companies in this branch...")
            companies = await self._search_and_extract(page, branch_name)
            all_companies.extend(companies)
            
            print(f"  Total so far: {len(all_companies)}")
        
        print(f"\n{'='*60}")
        print(f"Total companies scraped: {len(all_companies)}")
        print(f"{'='*60}")
        
        return all_companies
    
    async def _get_all_branches(self, page: Page) -> List[Tuple[str, str]]:
        """Extract all main branches from the dropdown"""
        branches = []
        
        try:
            # Find the branch selector dropdown
            branch_select = await page.query_selector('select[id*="branchSelector"]')
            if not branch_select:
                self._log("Could not find branch selector")
                return branches
            
            # Get all options
            options = await branch_select.query_selector_all('option')
            
            for option in options:
                value = await option.get_attribute('value')
                text = await option.text_content()
                
                # Skip empty or "all" option
                if value and value != "0" and text and text.strip() != "- alle -":
                    branches.append((value, text.strip()))
            
        except Exception as e:
            self._log(f"Error getting branches: {e}")
        
        return branches
    
    async def _get_sub_branches(self, page: Page) -> List[Tuple[str, str]]:
        """Not used - we extract all companies without sub-branch filtering"""
        return []
    
    async def _select_branch(self, page: Page, branch_value: str):
        """Select a main branch from the dropdown and wait for AJAX to complete"""
        try:
            branch_select = await page.query_selector('select[id*="branchSelector"]')
            if branch_select:
                self._log(f"Selecting branch with value: {branch_value}")
                
                # Select the branch - this triggers AJAX
                await branch_select.select_option(branch_value)
                
                # Wait for AJAX spinner/loading indicator if it appears
                await page.wait_for_timeout(500)
                
                # Wait for the AJAX request to complete by checking if sub-branch selector gets updated
                # The sub-branch dropdown should have its options updated
                try:
                    # Wait for network to be idle (AJAX completed)
                    await page.wait_for_load_state('networkidle', timeout=5000)
                except:
                    # If networkidle times out, just wait a bit
                    await page.wait_for_timeout(2000)
                    
        except Exception as e:
            self._log(f"Error selecting branch: {e}")
    
    async def _select_sub_branch(self, page: Page, sub_branch_value: str):
        """Select a sub-branch from the dropdown (unused - kept for compatibility)"""
        pass
    
    async def _search_and_extract(self, page: Page, branch_name: str) -> List[Tuple[str, str]]:
        """Search and extract companies for current branch"""
        companies = []
        
        try:
            # Click search button
            submit_button = await page.query_selector('button[id*="submitSearchButton"]')
            if submit_button:
                await submit_button.click()
                await page.wait_for_timeout(2000)
                
                # Set maximum results per page
                await self._set_max_results_per_page(page)
                
                # Extract companies from all pages
                page_num = 1
                max_pages = 100
                
                while page_num <= max_pages:
                    page_companies = await self._extract_companies_from_current_page(page, branch_name)
                    
                    if not page_companies:
                        break
                    
                    companies.extend(page_companies)
                    
                    # Try next page
                    if not await self._go_to_next_page(page):
                        break
                    
                    page_num += 1
                    await page.wait_for_timeout(1000)
        
        except Exception as e:
            self._log(f"Error in search and extract: {e}")
        
        return companies
    
    async def _set_max_results_per_page(self, page: Page):
        """Set maximum results per page"""
        try:
            # Look for results per page dropdown
            rpp_dropdown = await page.query_selector('select.ui-paginator-rpp-options')
            if rpp_dropdown:
                # Get all options and select the last one (highest value)
                options = await rpp_dropdown.query_selector_all('option')
                if options and len(options) > 0:
                    last_option = options[-1]
                    value = await last_option.get_attribute('value')
                    self._log(f"Setting results per page to: {value}")
                    await rpp_dropdown.select_option(value)
                    await page.wait_for_timeout(2000)
        except Exception as e:
            self._log(f"Could not set max results per page: {e}")
    
    async def _extract_companies_from_current_page(self, page: Page, branch_name: str) -> List[Tuple[str, str]]:
        """Extract company data from current page"""
        companies = []
        
        try:
            # Try multiple selectors for company rows
            selectors = [
                'tr[data-ri]',
                'tr.datarow',
                'tr[role="row"]',
                'table tbody tr:not(.ui-datatable-empty-message)',
            ]
            
            rows = None
            for selector in selectors:
                rows = await page.query_selector_all(selector)
                if rows and len(rows) > 0:
                    break
            
            if not rows:
                return companies
            
            for row in rows:
                try:
                    cells = await row.query_selector_all('td')
                    
                    if len(cells) >= 1:
                        texts = []
                        for cell in cells:
                            text = await cell.text_content()
                            texts.append((text or "").strip())
                        
                        if len(texts) >= 1:
                            name = texts[0]
                            
                            # Filter out headers
                            if name and not any(h in name.lower() for h in ['name', 'unternehmen', 'branche', 'no.']):
                                companies.append((name, branch_name))
                
                except Exception as e:
                    continue
        
        except Exception as e:
            self._log(f"Error extracting companies: {e}")
        
        return companies
    
    async def _go_to_next_page(self, page: Page) -> bool:
        """Try to navigate to the next page"""
        try:
            # PrimeFaces pagination selectors
            next_button = await page.query_selector('.ui-paginator-next:not(.ui-state-disabled)')
            
            if next_button:
                self._log("Clicking next button...")
                await next_button.click()
                await page.wait_for_timeout(2000)
                return True
            else:
                self._log("No active next button found")
                return False
                
        except Exception as e:
            self._log(f"Error navigating to next page: {e}")
            return False
        
    def save_to_csv(self, companies: List[Tuple[str, str]], filename: str = "furth_companies.csv"):
        """Save companies to CSV file with timestamp"""
        print(f"\nSaving {len(companies)} companies to {filename}...")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_companies = []
        for name, branch in companies:
            key = (name.lower(), branch.lower())
            if key not in seen:
                seen.add(key)
                unique_companies.append((name, branch))
        
        print(f"After removing duplicates: {len(unique_companies)} companies")
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name', 'Industry Branch'])
            
            for name, branch in unique_companies:
                writer.writerow([name, branch])
                
        # Also save JSON for easier programmatic access
        json_filename = filename.replace('.csv', '.json')
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_companies': len(unique_companies),
                'companies': [{'name': name, 'branch': branch} for name, branch in unique_companies]
            }, jsonfile, ensure_ascii=False, indent=2)
        
        print(f"Successfully saved to {filename}")
        print(f"Also saved JSON version to {json_filename}")


async def main():
    """Main function"""
    import sys
    
    # Parse command line arguments
    headless = '--show' not in sys.argv
    debug = '--debug' in sys.argv
    
    if debug:
        print("Debug mode enabled")
    
    if not headless:
        print("Browser window will be visible")
    
    scraper = FurthCompanyScraperAdvanced(headless=headless, debug=debug)
    companies = await scraper.scrape()
    scraper.save_to_csv(companies)
    
    print(f"\n=== Summary ===")
    print(f"Total companies scraped: {len(companies)}")
    
    if companies:
        print("\nFirst 10 companies:")
        for i, (name, branch) in enumerate(companies[:10], 1):
            print(f"  {i}. {name} | {branch}")
        
        print("\nSample branches:")
        branches = set(branch for _, branch in companies if branch)
        for branch in list(branches)[:10]:
            print(f"  - {branch}")


if __name__ == "__main__":
    asyncio.run(main())
