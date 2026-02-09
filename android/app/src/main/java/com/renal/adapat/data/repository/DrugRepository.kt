package com.renal.adapat.data.repository

import com.renal.adapat.data.database.DrugDao
import com.renal.adapat.data.database.entities.Drug
import com.renal.adapat.data.database.entities.Favorite
import com.renal.adapat.data.database.entities.History
import kotlinx.coroutines.flow.Flow

class DrugRepository(private val drugDao: DrugDao) {
    
    fun searchDrugs(query: String): Flow<List<Drug>> = drugDao.searchDrugs(query)
    
    suspend fun getDrugById(drugId: String): Drug? = drugDao.getDrugById(drugId)
    
    fun getAllDrugs(): Flow<List<Drug>> = drugDao.getAllDrugs()
    
    fun getFavorites(): Flow<List<Drug>> = drugDao.getFavorites()
    
    suspend fun isFavorite(drugId: String): Boolean = drugDao.isFavorite(drugId)
    
    suspend fun toggleFavorite(drugId: String) {
        if (isFavorite(drugId)) {
            drugDao.removeFavorite(drugId)
        } else {
            drugDao.addFavorite(Favorite(drugId))
        }
    }
    
    fun getHistory(): Flow<List<Drug>> = drugDao.getHistory()
    
    suspend fun addToHistory(drugId: String) {
        drugDao.addToHistory(History(drug_id = drugId))
    }
    
    suspend fun clearHistory() {
        drugDao.clearHistory()
    }
}
