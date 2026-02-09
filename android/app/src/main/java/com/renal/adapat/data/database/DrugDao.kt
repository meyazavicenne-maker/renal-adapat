package com.renal.adapat.data.database

import androidx.room.*
import com.renal.adapat.data.database.entities.Drug
import com.renal.adapat.data.database.entities.Favorite
import com.renal.adapat.data.database.entities.History
import kotlinx.coroutines.flow.Flow

@Dao
interface DrugDao {
    // Drug queries
    @Query("SELECT * FROM drugs WHERE name LIKE '%' || :query || '%' ORDER BY name")
    fun searchDrugs(query: String): Flow<List<Drug>>
    
    @Query("SELECT * FROM drugs WHERE id = :drugId")
    suspend fun getDrugById(drugId: String): Drug?
    
    @Query("SELECT * FROM drugs ORDER BY name")
    fun getAllDrugs(): Flow<List<Drug>>
    
    // Favorites
    @Query("SELECT drugs.* FROM drugs INNER JOIN favorites ON drugs.id = favorites.drug_id ORDER BY favorites.timestamp DESC")
    fun getFavorites(): Flow<List<Drug>>
    
    @Query("SELECT EXISTS(SELECT 1 FROM favorites WHERE drug_id = :drugId)")
    suspend fun isFavorite(drugId: String): Boolean
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun addFavorite(favorite: Favorite)
    
    @Query("DELETE FROM favorites WHERE drug_id = :drugId")
    suspend fun removeFavorite(drugId: String)
    
    // History
    @Query("SELECT DISTINCT drugs.* FROM drugs INNER JOIN history ON drugs.id = history.drug_id ORDER BY history.timestamp DESC LIMIT 20")
    fun getHistory(): Flow<List<Drug>>
    
    @Insert
    suspend fun addToHistory(history: History)
    
    @Query("DELETE FROM history")
    suspend fun clearHistory()
}
