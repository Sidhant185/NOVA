"""
Search API endpoints
Handles real-time web search using DuckDuckGo
"""
from flask import Blueprint, request, jsonify
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

bp = Blueprint('search', __name__)

@bp.route('', methods=['POST'])
def search():
    """Perform web search."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        query = data.get('query', '').strip()
        max_results = data.get('max_results', 5)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Perform search using DuckDuckGo
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return jsonify({
                'success': True,
                'query': query,
                'results': [],
                'count': 0,
                'message': f'No results found for "{query}"'
            })
        
        # Format results
        formatted_results = []
        for i, res in enumerate(results, start=1):
            formatted_results.append({
                'index': i,
                'title': res.get('title', ''),
                'snippet': res.get('body', ''),
                'url': res.get('href', ''),
                'relevance': res.get('relevance', 0)
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'results': formatted_results,
            'count': len(formatted_results)
        })
    
    except Exception as e:
        logger.error(f"Error in search: {e}", exc_info=True)
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@bp.route('/suggest', methods=['GET'])
def suggest():
    """Get search suggestions (autocomplete)."""
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 2:
            return jsonify({
                'success': True,
                'suggestions': []
            })
        
        # Use DuckDuckGo for suggestions
        with DDGS() as ddgs:
            suggestions = list(ddgs.suggestions(query))
        
        formatted_suggestions = [s.get('phrase', '') for s in suggestions[:5]]
        
        return jsonify({
            'success': True,
            'query': query,
            'suggestions': formatted_suggestions
        })
    
    except Exception as e:
        logger.error(f"Error in suggest: {e}", exc_info=True)
        return jsonify({'error': f'Suggestion failed: {str(e)}'}), 500

