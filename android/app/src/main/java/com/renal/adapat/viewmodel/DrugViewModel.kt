package com.renal.adapat.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.renal.adapat.data.database.DrugDatabase
import com.renal.adapat.data.database.entities.Drug
import com.renal.adapat.data.repository.DrugRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class DrugViewModel(application: Application) : AndroidViewModel(application) {
    private val repository: DrugRepository
    
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()
    
    val searchResults: StateFlow<List<Drug>> = searchQuery
        .debounce(300)
        .flatMapLatest { query ->
            if (query.length >= 2) {
                repository.searchDrugs(query)
            } else {
                flowOf(emptyList())
            }
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )
    
    val favorites: StateFlow<List<Drug>>
    val history: StateFlow<List<Drug>>
    
    init {
        val database = DrugDatabase.getDatabase(application)
        repository = DrugRepository(database.drugDao())
        
        favorites = repository.getFavorites()
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5000),
                initialValue = emptyList()
            )
        
        history = repository.getHistory()
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5000),
                initialValue = emptyList()
            )
    }
    
    fun updateSearchQuery(query: String) {
        _searchQuery.value = query
    }
    
    suspend fun getDrugById(drugId: String): Drug? {
        return repository.getDrugById(drugId)
    }
    
    suspend fun isFavorite(drugId: String): Boolean {
        return repository.isFavorite(drugId)
    }
    
    fun toggleFavorite(drugId: String) {
        viewModelScope.launch {
            repository.toggleFavorite(drugId)
        }
    }
    
    fun addToHistory(drugId: String) {
        viewModelScope.launch {
            repository.addToHistory(drugId)
        }
    }
    
    fun clearHistory() {
        viewModelScope.launch {
            repository.clearHistory()
        }
    }
}
