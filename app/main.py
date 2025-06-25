def main():
    """Fonction principale"""
    print(" === : MODÉLISATION LILLE 4 PIÈCES ===\n")
    
    #  Charger et explorer
    df = load_and_explore_data()
    
    #  Filtrer 4 pièces
    df_4p = filter_4_pieces_data(df)
    
    if df_4p is None:
        return
    
    #  Séparer appartements/maisons
    appartements, maisons = create_separate_datasets(df_4p)
    
    #  Nettoyer et préparer les données
    X_apt, y_apt, df_apt_clean = select_features_and_clean(appartements, "APPARTEMENTS")
    X_maisons, y_maisons, df_maisons_clean = select_features_and_clean(maisons, "MAISONS")
    
    #  Entraîner les modèles
    appartements_results = train_models(X_apt, y_apt, "APPARTEMENTS")
    maisons_results = train_models(X_maisons, y_maisons, "MAISONS")
    
    #  Comparer les résultats
    display_results_comparison(appartements_results, maisons_results)
    
if __name__ == "__main__":
    main()