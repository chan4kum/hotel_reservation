from scipy.stats import randint,uniform

LIGHTGM_PARAMS = {
    'n_estimators': randint(50, 200),
    'learning_rate': uniform(0.01, 0.2),
    'num_leaves': randint(20, 100),
    'max_depth': randint(5, 50),
    'boosting_type': ['gbdt','dart','goss']
}

RANDOM_SEARCH_PARAMS= {
    'n_iter': 4,
    'cv': 5,
    'verbose': 2,
    'random_state': 42,
    'n_jobs': -1,
    'scoring': 'accuracy'
}