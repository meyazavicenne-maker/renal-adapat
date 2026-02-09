package com.renal.adapat.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.renal.adapat.data.database.entities.Drug
import com.renal.adapat.ui.theme.*
import com.renal.adapat.viewmodel.DrugViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DrugDetailsScreen(
    drugId: String,
    navController: NavController,
    viewModel: DrugViewModel = viewModel()
) {
    var drug by remember { mutableStateOf<Drug?>(null) }
    var isFavorite by remember { mutableStateOf(false) }
    
    LaunchedEffect(drugId) {
        drug = viewModel.getDrugById(drugId)
        isFavorite = viewModel.isFavorite(drugId)
    }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(drug?.name ?: "Chargement...") },
                navigationIcon = {
                    IconButton(onClick = { navController.navigateUp() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = {
                        viewModel.toggleFavorite(drugId)
                        isFavorite = !isFavorite
                    }) {
                        Icon(
                            if (isFavorite) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                            contentDescription = "Toggle favorite",
                            tint = if (isFavorite) PrimaryLight else Surface
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Primary,
                    titleContentColor = Surface,
                    navigationIconContentColor = Surface
                )
            )
        }
    ) { paddingValues ->
        drug?.let { currentDrug ->
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Category
                if (!currentDrug.category.isNullOrBlank()) {
                    item {
                        Text(
                            text = currentDrug.category,
                            style = MaterialTheme.typography.titleMedium,
                            color = TextSecondary
                        )
                    }
                }
                
                // Normal dose
                if (!currentDrug.dose_normal.isNullOrBlank()) {
                    item {
                        InfoCard(
                            title = "Posologie normale",
                            content = currentDrug.dose_normal,
                            backgroundColor = InfoBackground,
                            textColor = InfoText,
                            icon = Icons.Default.MedicalServices
                        )
                    }
                }
                
                // Renal impairment dose
                if (!currentDrug.dose_renal_impairment.isNullOrBlank()) {
                    item {
                        InfoCard(
                            title = "Dose en insuffisance rénale",
                            content = currentDrug.dose_renal_impairment,
                            backgroundColor = WarningBackground,
                            textColor = WarningText,
                            icon = Icons.Default.Warning
                        )
                    }
                }
                
                // Replacement therapy dose
                if (!currentDrug.dose_replacement.isNullOrBlank()) {
                    item {
                        InfoCard(
                            title = "Dose en thérapie de remplacement",
                            content = currentDrug.dose_replacement,
                            backgroundColor = InfoBackground,
                            textColor = InfoText,
                            icon = Icons.Default.Autorenew
                        )
                    }
                }
                
                // Warnings
                if (!currentDrug.warnings.isNullOrBlank()) {
                    item {
                        InfoCard(
                            title = "Avertissements",
                            content = currentDrug.warnings,
                            backgroundColor = ErrorBackground,
                            textColor = ErrorText,
                            icon = Icons.Default.ReportProblem
                        )
                    }
                }
                
                // Interactions
                if (!currentDrug.interactions.isNullOrBlank()) {
                    item {
                        InfoCard(
                            title = "Interactions",
                            content = currentDrug.interactions,
                            backgroundColor = InfoBackground,
                            textColor = InfoText,
                            icon = Icons.Default.SwapHoriz
                        )
                    }
                }
                
                // Notes
                if (!currentDrug.notes.isNullOrBlank()) {
                    item {
                        InfoCard(
                            title = "Notes",
                            content = currentDrug.notes,
                            backgroundColor = Surface,
                            textColor = TextPrimary,
                            icon = Icons.Default.Notes
                        )
                    }
                }
            }
        } ?: run {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = androidx.compose.ui.Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        }
    }
}

@Composable
fun InfoCard(
    title: String,
    content: String,
    backgroundColor: androidx.compose.ui.graphics.Color,
    textColor: androidx.compose.ui.graphics.Color,
    icon: androidx.compose.ui.graphics.vector.ImageVector
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .background(backgroundColor)
                .padding(16.dp)
        ) {
            Row(
                verticalAlignment = androidx.compose.ui.Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = title,
                    tint = textColor,
                    modifier = Modifier.size(24.dp)
                )
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    color = textColor
                )
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            Text(
                text = content,
                style = MaterialTheme.typography.bodyLarge, // Larger text for readability
                color = TextPrimary
            )
        }
    }
}
