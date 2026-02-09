package com.renal.adapat.data.database.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "drugs")
data class Drug(
    @PrimaryKey val id: String,
    val name: String,
    val category: String?,
    val dose_normal: String?,
    val dose_renal_impairment: String?,
    val dose_replacement: String?,
    val warnings: String?,
    val interactions: String?,
    val notes: String?
)

@Entity(tableName = "favorites")
data class Favorite(
    @PrimaryKey val drug_id: String,
    val timestamp: Long = System.currentTimeMillis()
)

@Entity(tableName = "history")
data class History(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val drug_id: String,
    val timestamp: Long = System.currentTimeMillis()
)
