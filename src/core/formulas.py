import math

def convert_creat_to_mgdl(value, unit):
    """
    Converts creatinine value to mg/dL.
    Supported units: 'mg/L', 'mg/dL', 'µmol/L'
    """
    if unit == 'mg/dL':
        return value
    elif unit == 'mg/L':
        return value / 10.0
    elif unit == 'µmol/L':
        return value / 88.4
    else:
        raise ValueError(f"Unknown unit: {unit}")

def calculate_cockcroft_gault(age, weight, creat_mgdl, sex):
    """
    Cockcroft-Gault Formula
    ((140 - Age) * Weight) / (72 * Cr) [* 0.85 if Female]
    Returns mL/min
    """
    if creat_mgdl <= 0: return 0
    
    gfr = ((140 - age) * weight) / (72 * creat_mgdl)
    
    if sex == 'F':
        gfr *= 0.85
        
    return gfr

def calculate_mdrd(age, creat_mgdl, sex, race_black=False):
    """
    MDRD (4-variable IDMS traceable)
    175 * (Cr)^-1.154 * (Age)^-0.203 [* 0.742 if Female] [* 1.212 if Black]
    Returns mL/min/1.73m^2
    """
    if creat_mgdl <= 0: return 0
    
    gfr = 175 * (creat_mgdl ** -1.154) * (age ** -0.203)
    
    if sex == 'F':
        gfr *= 0.742
    if race_black:
        gfr *= 1.212
        
    return gfr

def calculate_ckd_epi(age, creat_mgdl, sex, race_black=False):
    """
    CKD-EPI (2009)
    Returns mL/min/1.73m^2
    """
    if creat_mgdl <= 0: return 0
    
    k = 0.7 if sex == 'F' else 0.9
    alpha = -0.329 if sex == 'F' else -0.411
    
    # Min(Cr/k, 1)^alpha * Max(Cr/k, 1)^-1.209
    ratio = creat_mgdl / k
    
    term1 = min(ratio, 1) ** alpha
    term2 = max(ratio, 1) ** -1.209
    term3 = 0.993 ** age
    
    gfr = 141 * term1 * term2 * term3
    
    if sex == 'F':
        gfr *= 1.018
    if race_black:
        gfr *= 1.159
        
    return gfr

def calculate_schwartz(height_cm, creat_mgdl):
    """
    Bedside Schwartz (2009)
    0.413 * Height(cm) / Cr_mgdl
    Returns mL/min/1.73m^2
    """
    if creat_mgdl <= 0: return 0
    if not height_cm: return 0
    
    return (0.413 * height_cm) / creat_mgdl

def calculate_corrected_sodium(measured_na, glucose_mgdl):
    """
    Corrected Sodium (Katz, 1973)
    Na + 0.016 * (Glucose - 100)
    """
    if measured_na <= 0: return 0
    return measured_na + 0.016 * (glucose_mgdl - 100)

def calculate_water_deficit(weight, measured_na, sex='M', age_group='adult'):
    """
    Free Water Deficit
    FWD = TBW * ((Na / 140) - 1)
    """
    if measured_na <= 140: return 0
    
    # Estimate TBW
    if sex == 'M':
        k = 0.6 if age_group == 'adult' else 0.5
    else:
        k = 0.5 if age_group == 'adult' else 0.45
        
    tbw = weight * k
    return tbw * ((measured_na / 140.0) - 1)

def calculate_anion_gap(na, k, cl, hco3):
    """
    Anion Gap = (Na + K) - (Cl + HCO3)
    """
    if na <= 0: return 0
    return (na + k) - (cl + hco3)

def calculate_ktv_daugirdas(pre_bun, post_bun, weight, uf_volume, hours):
    """
    spKt/V Daugirdas II
    -ln(R - 0.008*t) + (4 - 3.5*R) * (UF/W)
    R = post_bun/pre_bun
    """
    if pre_bun <= 0 or weight <= 0: return 0
    
    r = post_bun / pre_bun
    # Ensure R - 0.008t is > 0 for log
    log_arg = r - 0.008 * hours
    if log_arg <= 0: log_arg = 0.0001
    
    ktv = -math.log(log_arg) + (4 - 3.5 * r) * (uf_volume / weight)
    return ktv

def calculate_corrected_calcium(measured_ca_mgl, albumin_gl):
    """
    Corrected Calcium (Albumin)
    Formula: Ca_corr = Ca_measured + 0.8 * (40 - Albumin)
    Using mg/L for Calcium and g/L for Albumin
    """
    if measured_ca_mgl <= 0: return 0
    return measured_ca_mgl + 0.8 * (40 - albumin_gl)

def calculate_iron_deficit(weight, actual_hb, target_hb, is_adult=True):
    """
    Ganzoni Formula
    Iron Deficit (mg) = [Weight(kg) x (Target Hb - Actual Hb)(g/dL) x 2.4] + Stores
    Stores: 500mg (adults) or 15mg/kg (children)
    """
    if weight <= 0: return 0
    
    hb_deficit = target_hb - actual_hb
    if hb_deficit <= 0: return 0
    
    stores = 500 if is_adult else (15 * weight)
    
    total_deficit = (weight * hb_deficit * 2.4) + stores
    return total_deficit
