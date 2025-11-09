/**
 * Offline Manager - Handles online/offline detection and local caching
 *
 * Features:
 * - Detects online/offline status
 * - Caches recipe database when online
 * - Serves cached data when offline
 * - Disables CRUD operations when offline
 * - Shows visual status indicators
 */

class OfflineManager {
  constructor() {
    this.CACHE_KEY = 'fergi_recipes_cache';
    this.CACHE_TIMESTAMP_KEY = 'fergi_recipes_cache_timestamp';
    this.CACHE_EXPIRY_HOURS = 24; // Re-fetch after 24 hours
    this.isOnline = navigator.onLine;

    // Set up event listeners for online/offline
    window.addEventListener('online', () => this.handleOnline());
    window.addEventListener('offline', () => this.handleOffline());

    console.log(`📡 Offline Manager initialized - Status: ${this.isOnline ? 'Online' : 'Offline'}`);
  }

  /**
   * Check if browser is currently online
   */
  isOnlineNow() {
    return navigator.onLine;
  }

  /**
   * Handle coming online
   */
  handleOnline() {
    this.isOnline = true;
    console.log('✅ Connection restored - Online');
    this.updateStatusUI();

    // Automatically refresh cache when coming online
    this.refreshCacheIfNeeded();
  }

  /**
   * Handle going offline
   */
  handleOffline() {
    this.isOnline = false;
    console.log('⚠️ Connection lost - Offline mode');
    this.updateStatusUI();
  }

  /**
   * Update UI to show online/offline status
   */
  updateStatusUI() {
    const indicator = document.getElementById('connection-status');
    if (!indicator) return;

    if (this.isOnline) {
      indicator.className = 'status-online';
      indicator.innerHTML = '🟢 Online';
    } else {
      indicator.className = 'status-offline';
      indicator.innerHTML = '🔴 Offline - Read Only';
    }
  }

  /**
   * Enable/disable CRUD buttons based on online status
   */
  updateCRUDButtons() {
    const crudButtons = document.querySelectorAll('[data-requires-online="true"]');

    crudButtons.forEach(button => {
      if (this.isOnline) {
        button.disabled = false;
        button.classList.remove('disabled-offline');
        button.title = '';
      } else {
        button.disabled = true;
        button.classList.add('disabled-offline');
        button.title = 'Requires internet connection';
      }
    });
  }

  /**
   * Fetch recipes from API (when online)
   */
  async fetchRecipesFromAPI() {
    if (!this.isOnline) {
      throw new Error('Cannot fetch - offline');
    }

    console.log('📥 Fetching recipes from API...');

    // Try load-recipes first (Dropbox), fallback to get-recipes
    try {
      const response = await fetch('/.netlify/functions/load-recipes');
      if (response.ok) {
        const data = await response.json();
        return data.recipes;
      }
    } catch (error) {
      console.warn('⚠️ load-recipes failed, trying get-recipes:', error);
    }

    // Fallback to get-recipes
    const response = await fetch('/.netlify/functions/get-recipes');
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    return data.recipes;
  }

  /**
   * Cache recipes to localStorage
   */
  cacheRecipes(recipes) {
    try {
      localStorage.setItem(this.CACHE_KEY, JSON.stringify(recipes));
      localStorage.setItem(this.CACHE_TIMESTAMP_KEY, Date.now().toString());
      console.log(`💾 Cached ${recipes.length} recipes locally`);
      return true;
    } catch (error) {
      console.error('❌ Failed to cache recipes:', error);
      return false;
    }
  }

  /**
   * Load recipes from cache
   */
  loadFromCache() {
    try {
      const cached = localStorage.getItem(this.CACHE_KEY);
      if (!cached) {
        console.log('ℹ️ No cached recipes found');
        return null;
      }

      const recipes = JSON.parse(cached);
      console.log(`📂 Loaded ${recipes.length} recipes from cache`);
      return recipes;
    } catch (error) {
      console.error('❌ Failed to load cache:', error);
      return null;
    }
  }

  /**
   * Check if cache exists and is valid
   */
  isCacheValid() {
    const timestamp = localStorage.getItem(this.CACHE_TIMESTAMP_KEY);
    if (!timestamp) return false;

    const age = Date.now() - parseInt(timestamp);
    const maxAge = this.CACHE_EXPIRY_HOURS * 60 * 60 * 1000;

    return age < maxAge;
  }

  /**
   * Get cache age in human-readable format
   */
  getCacheAge() {
    const timestamp = localStorage.getItem(this.CACHE_TIMESTAMP_KEY);
    if (!timestamp) return 'No cache';

    const age = Date.now() - parseInt(timestamp);
    const hours = Math.floor(age / (60 * 60 * 1000));
    const minutes = Math.floor((age % (60 * 60 * 1000)) / (60 * 1000));

    if (hours > 0) return `${hours}h ${minutes}m ago`;
    return `${minutes}m ago`;
  }

  /**
   * Refresh cache if needed (expired or doesn't exist)
   */
  async refreshCacheIfNeeded() {
    if (!this.isOnline) {
      console.log('⏸️ Skipping cache refresh - offline');
      return false;
    }

    if (this.isCacheValid()) {
      console.log(`✅ Cache is fresh (${this.getCacheAge()})`);
      return false;
    }

    console.log('🔄 Cache expired or missing - refreshing...');
    return await this.refreshCache();
  }

  /**
   * Force refresh cache from API
   */
  async refreshCache() {
    if (!this.isOnline) {
      console.log('❌ Cannot refresh - offline');
      return false;
    }

    try {
      const recipes = await this.fetchRecipesFromAPI();
      this.cacheRecipes(recipes);
      return true;
    } catch (error) {
      console.error('❌ Failed to refresh cache:', error);
      return false;
    }
  }

  /**
   * Get recipes - tries API first, falls back to cache
   */
  async getRecipes() {
    // If online, try API first
    if (this.isOnline) {
      try {
        console.log('🌐 Online - fetching from API');
        const recipes = await this.fetchRecipesFromAPI();
        this.cacheRecipes(recipes); // Update cache
        return {
          recipes,
          source: 'api',
          cached: false
        };
      } catch (error) {
        console.warn('⚠️ API failed, falling back to cache:', error);
        // Fall through to cache
      }
    }

    // Offline or API failed - use cache
    console.log('📂 Loading from cache');
    const recipes = this.loadFromCache();

    if (!recipes) {
      throw new Error('No cached data available and cannot fetch (offline)');
    }

    return {
      recipes,
      source: 'cache',
      cached: true,
      cacheAge: this.getCacheAge()
    };
  }

  /**
   * Clear all cached data
   */
  clearCache() {
    localStorage.removeItem(this.CACHE_KEY);
    localStorage.removeItem(this.CACHE_TIMESTAMP_KEY);
    console.log('🗑️ Cache cleared');
  }

  /**
   * Get cache statistics
   */
  getCacheStats() {
    const cached = this.loadFromCache();
    const timestamp = localStorage.getItem(this.CACHE_TIMESTAMP_KEY);

    return {
      exists: !!cached,
      count: cached ? cached.length : 0,
      age: this.getCacheAge(),
      valid: this.isCacheValid(),
      timestamp: timestamp ? new Date(parseInt(timestamp)) : null
    };
  }
}

// Create global instance
window.offlineManager = new OfflineManager();
