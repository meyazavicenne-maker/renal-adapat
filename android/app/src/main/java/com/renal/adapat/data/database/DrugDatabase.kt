package com.renal.adapat.data.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.renal.adapat.data.database.entities.Drug
import com.renal.adapat.data.database.entities.Favorite
import com.renal.adapat.data.database.entities.History

@Database(
    entities = [Drug::class, Favorite::class, History::class],
    version = 1,
    exportSchema = false
)
abstract class DrugDatabase : RoomDatabase() {
    abstract fun drugDao(): DrugDao
    
    companion object {
        @Volatile
        private var INSTANCE: DrugDatabase? = null
        
        fun getDatabase(context: Context): DrugDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    DrugDatabase::class.java,
                    "renal_drugs.db"
                )
                .createFromAsset("renal_drugs.db") // Copy from assets folder
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
