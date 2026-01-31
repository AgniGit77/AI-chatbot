"""
Product information service for fetching and processing product data
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

class ProductService:
    """Service for fetching product information from URLs"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_product_info(self, product_url):
        """
        Extract product information from URL
        
        Args:
            product_url: URL of the product page
            
        Returns:
            dict: Product information including name, price, images, etc.
        """
        try:
            # Determine the retailer
            domain = urlparse(product_url).netloc
            
            # Try to fetch and parse the page
            response = requests.get(product_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract basic information (generic extraction)
                product_info = {
                    'url': product_url,
                    'name': self._extract_product_name(soup),
                    'price': self._extract_price(soup),
                    'images': self._extract_images(soup),
                    'description': self._extract_description(soup),
                    'sizes': self._extract_sizes(soup),
                    'colors': self._extract_colors(soup),
                    'category': self._extract_category(soup),
                    'brand': self._extract_brand(soup),
                    'retailer': domain
                }
                
                return product_info
            else:
                # Return mock data if fetching fails
                return self._get_mock_product_data(product_url)
                
        except Exception as e:
            print(f"Error fetching product info: {e}")
            # Return mock data on error
            return self._get_mock_product_data(product_url)
    
    def _extract_product_name(self, soup):
        """Extract product name from HTML"""
        # Try common selectors
        selectors = [
            {'name': 'h1'},
            {'class_': re.compile('product.*title', re.I)},
            {'class_': re.compile('product.*name', re.I)},
            {'property': 'og:title'}
        ]
        
        for selector in selectors:
            element = soup.find(attrs=selector)
            if element:
                return element.get_text(strip=True)
        
        return "Fashion Item"
    
    def _extract_price(self, soup):
        """Extract price from HTML"""
        # Try common price selectors
        price_patterns = [
            {'class_': re.compile('price', re.I)},
            {'property': 'og:price:amount'},
            {'itemprop': 'price'}
        ]
        
        for pattern in price_patterns:
            element = soup.find(attrs=pattern)
            if element:
                price_text = element.get_text(strip=True) if hasattr(element, 'get_text') else element.get('content', '')
                # Extract numeric value
                price_match = re.search(r'[\d,]+\.?\d*', price_text)
                if price_match:
                    return f"${price_match.group()}"
        
        return "$0.00"
    
    def _extract_images(self, soup):
        """Extract product images from HTML"""
        images = []
        
        # Try og:image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            images.append(og_image['content'])
        
        # Try product image selectors
        img_elements = soup.find_all('img', class_=re.compile('product', re.I))
        for img in img_elements[:5]:  # Limit to 5 images
            if img.get('src'):
                images.append(img['src'])
        
        return images if images else ['/static/images/placeholder.jpg']
    
    def _extract_description(self, soup):
        """Extract product description"""
        desc_selectors = [
            {'class_': re.compile('description', re.I)},
            {'class_': re.compile('product.*detail', re.I)},
            {'property': 'og:description'}
        ]
        
        for selector in desc_selectors:
            element = soup.find(attrs=selector)
            if element:
                text = element.get_text(strip=True) if hasattr(element, 'get_text') else element.get('content', '')
                if text:
                    return text[:500]  # Limit length
        
        return "Fashion item available for purchase"
    
    def _extract_sizes(self, soup):
        """Extract available sizes"""
        # Try to find size selectors
        size_select = soup.find('select', {'name': re.compile('size', re.I)})
        if size_select:
            options = size_select.find_all('option')
            return [opt.get_text(strip=True) for opt in options if opt.get_text(strip=True)]
        
        return ['XS', 'S', 'M', 'L', 'XL']
    
    def _extract_colors(self, soup):
        """Extract available colors"""
        # Try to find color selectors
        color_elements = soup.find_all(attrs={'class': re.compile('color', re.I)})
        colors = []
        for elem in color_elements[:10]:
            color_text = elem.get_text(strip=True)
            if color_text and len(color_text) < 30:
                colors.append(color_text)
        
        return colors if colors else ['Available in multiple colors']
    
    def _extract_category(self, soup):
        """Extract product category"""
        # Try breadcrumbs or category tags
        breadcrumb = soup.find(attrs={'class': re.compile('breadcrumb', re.I)})
        if breadcrumb:
            return breadcrumb.get_text(strip=True)
        
        return 'Clothing'
    
    def _extract_brand(self, soup):
        """Extract brand name"""
        brand_selectors = [
            {'class_': re.compile('brand', re.I)},
            {'itemprop': 'brand'}
        ]
        
        for selector in brand_selectors:
            element = soup.find(attrs=selector)
            if element:
                return element.get_text(strip=True)
        
        return 'Fashion Brand'
    
    def _get_mock_product_data(self, url):
        """Return mock product data when actual fetching fails"""
        return {
            'url': url,
            'name': 'Stylish Fashion Item',
            'price': '$49.99',
            'images': ['/static/images/placeholder.jpg'],
            'description': 'A beautiful fashion item perfect for any occasion',
            'sizes': ['XS', 'S', 'M', 'L', 'XL'],
            'colors': ['Black', 'White', 'Navy'],
            'category': 'Clothing',
            'brand': 'Fashion Brand',
            'retailer': urlparse(url).netloc
        }
    
    def search_similar_products(self, product_info, price_range=None):
        """
        Search for similar products
        
        Args:
            product_info: Original product information
            price_range: Optional price range filter
            
        Returns:
            list: Similar product suggestions
        """
        # Simulate product search (in production, use actual search API)
        similar_products = [
            {
                'name': f"Similar {product_info['category']} Style 1",
                'price': '$44.99',
                'url': 'https://example.com/product1',
                'image': '/static/images/placeholder.jpg',
                'reason': 'Similar style and fit'
            },
            {
                'name': f"Alternative {product_info['category']} Option",
                'price': '$39.99',
                'url': 'https://example.com/product2',
                'image': '/static/images/placeholder.jpg',
                'reason': 'More affordable alternative'
            },
            {
                'name': f"Premium {product_info['category']} Version",
                'price': '$79.99',
                'url': 'https://example.com/product3',
                'image': '/static/images/placeholder.jpg',
                'reason': 'Higher quality materials'
            }
        ]
        
        return similar_products
