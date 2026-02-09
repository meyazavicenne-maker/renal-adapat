package com.renal.adapat

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.renal.adapat.ui.screens.*
import com.renal.adapat.ui.theme.RenalAdapatTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            RenalAdapatTheme {
                MainScreen()
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route
    
    val items = listOf(
        NavigationItem("home", "Accueil", Icons.Default.Home),
        NavigationItem("search", "Recherche", Icons.Default.Search),
        NavigationItem("favorites", "Favoris", Icons.Default.Favorite),
        NavigationItem("history", "Historique", Icons.Default.History),
        NavigationItem("calculator", "Calcul", Icons.Default.Calculate)
    )
    
    // Handle Android back button
    androidx.activity.compose.BackHandler(enabled = currentRoute != "home") {
        navController.navigateUp()
    }
    
    Scaffold(
        bottomBar = {
            NavigationBar {
                items.forEach { item ->
                    NavigationBarItem(
                        icon = { Icon(item.icon, contentDescription = item.label) },
                        label = { Text(item.label) },
                        selected = currentRoute == item.route,
                        onClick = {
                            navController.navigate(item.route) {
                                popUpTo(navController.graph.startDestinationId) {
                                    saveState = true
                                }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    )
                }
            }
        }
    ) { paddingValues ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(paddingValues)
        ) {
            composable("home") { HomeScreen(navController) }
            composable("search") { SearchScreen(navController) }
            composable("favorites") { FavoritesScreen(navController) }
            composable("history") { HistoryScreen(navController) }
            composable("calculator") { CalculatorScreen() }
            composable("drug/{drugId}") { backStackEntry ->
                val drugId = backStackEntry.arguments?.getString("drugId") ?: return@composable
                DrugDetailsScreen(drugId, navController)
            }
        }
    }
}

data class NavigationItem(
    val route: String,
    val label: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector
)
