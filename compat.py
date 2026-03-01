"""
Python 3.9 Compatibility Module
Patches importlib.metadata for packages_distributions compatibility

This module provides a compatibility layer for Python 3.9 by:
1. First trying to use the importlib_metadata backport package (recommended)
2. Falling back to an optimized cached implementation if backport unavailable
"""
import sys

# Module-level cache for packages_distributions results
_packages_distributions_cache = None

# Python 3.9 compatibility fix for importlib.metadata.packages_distributions
# This must be done before any other imports that might use importlib.metadata
if sys.version_info < (3, 10):
    try:
        import importlib.metadata
        
        # Strategy 1: Try to use importlib_metadata backport (recommended)
        try:
            import importlib_metadata
            # Patch importlib.metadata to use the backport's packages_distributions
            if hasattr(importlib_metadata, 'packages_distributions'):
                importlib.metadata.packages_distributions = importlib_metadata.packages_distributions
            elif hasattr(importlib_metadata.metadata, 'packages_distributions'):
                importlib.metadata.packages_distributions = importlib_metadata.metadata.packages_distributions
        except ImportError:
            # importlib_metadata not installed, use fallback implementation
            pass
        
        # Strategy 2: Fallback to optimized cached implementation
        if not hasattr(importlib.metadata, 'packages_distributions'):
            def packages_distributions():
                """
                Optimized backport of importlib.metadata.packages_distributions for Python < 3.10.
                Uses caching to avoid recomputing on every call.
                """
                global _packages_distributions_cache
                
                # Return cached result if available
                if _packages_distributions_cache is not None:
                    return _packages_distributions_cache.copy()
                
                distributions = {}
                try:
                    # Use a set to track processed distributions for faster lookups
                    processed_distributions = set()
                    
                    for dist in importlib.metadata.distributions():
                        try:
                            # Get distribution name
                            dist_name = dist.metadata.get('Name', '')
                            if not dist_name or dist_name in processed_distributions:
                                continue
                            
                            processed_distributions.add(dist_name)
                            
                            # Try to read top_level.txt with error handling
                            try:
                                top_level_content = dist.read_text('top_level.txt')
                            except (FileNotFoundError, OSError, PermissionError):
                                # Skip distributions without top_level.txt or permission issues
                                continue
                            
                            if top_level_content:
                                # Split by whitespace (handles both newlines and spaces)
                                packages = top_level_content.strip().split()
                                for package in packages:
                                    package = package.strip()
                                    if package:
                                        if package not in distributions:
                                            distributions[package] = []
                                        # Avoid duplicates
                                        if dist_name not in distributions[package]:
                                            distributions[package].append(dist_name)
                        except (KeyError, AttributeError, TypeError, ValueError):
                            # Skip distributions with invalid metadata
                            continue
                        except Exception:
                            # Skip any other unexpected errors to prevent hanging
                            continue
                except Exception:
                    # Return empty dict if something goes wrong
                    distributions = {}
                
                # Cache the result
                _packages_distributions_cache = distributions.copy()
                return distributions
            
            # Add as function to importlib.metadata
            importlib.metadata.packages_distributions = packages_distributions
    except Exception:
        # If anything fails, silently continue - the app will work without this patch
        # but may show warnings about Python version
        pass
