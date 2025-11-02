"""
Flask web server - REST API and web interface for recipe database
"""

from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS
from database import RecipeDatabase
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for API access

# Database instance
db = RecipeDatabase()

# Configuration
RECIPES_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================================
# API Endpoints
# ============================================================================

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes (summary view)"""
    try:
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', default=0, type=int)
        search = request.args.get('search', default='', type=str)

        if search:
            recipes = db.search_recipes(search)
        else:
            recipes = db.get_all_recipes(limit=limit, offset=offset)

        return jsonify({
            'success': True,
            'count': len(recipes),
            'recipes': recipes
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """Get single recipe with full details"""
    try:
        recipe = db.get_recipe(recipe_id)

        if not recipe:
            return jsonify({'success': False, 'error': 'Recipe not found'}), 404

        return jsonify({
            'success': True,
            'recipe': recipe
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    """Create new recipe"""
    try:
        recipe_data = request.json

        if not recipe_data or 'title' not in recipe_data:
            return jsonify({'success': False, 'error': 'Title is required'}), 400

        recipe_id = db.add_recipe(recipe_data)

        return jsonify({
            'success': True,
            'recipe_id': recipe_id,
            'message': 'Recipe created successfully'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    """Update existing recipe"""
    try:
        recipe_data = request.json

        if not recipe_data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        success = db.update_recipe(recipe_id, recipe_data)

        if success:
            return jsonify({
                'success': True,
                'message': 'Recipe updated successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Update failed'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """Delete recipe"""
    try:
        success = db.delete_recipe(recipe_id)

        if success:
            return jsonify({
                'success': True,
                'message': 'Recipe deleted successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Delete failed'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get database statistics"""
    try:
        stats = db.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/search', methods=['GET'])
def search_recipes():
    """Search recipes"""
    try:
        query = request.args.get('q', default='', type=str)

        if not query:
            return jsonify({'success': False, 'error': 'Search query required'}), 400

        recipes = db.search_recipes(query)

        return jsonify({
            'success': True,
            'count': len(recipes),
            'recipes': recipes
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# Web Interface Routes
# ============================================================================

@app.route('/')
def index():
    """Serve main web interface"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ============================================================================
# Main
# ============================================================================

def main():
    """Start the server"""
    import argparse

    parser = argparse.ArgumentParser(description='Recipe database web server')
    parser.add_argument('--host', default='127.0.0.1',
                       help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("Recipe Database Server")
    print(f"{'='*60}")
    print(f"Server starting at: http://{args.host}:{args.port}")
    print(f"API endpoint: http://{args.host}:{args.port}/api")
    print(f"{'='*60}\n")

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
