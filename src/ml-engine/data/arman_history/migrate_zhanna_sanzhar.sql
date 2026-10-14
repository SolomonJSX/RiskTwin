-- 1. accounts
INSERT INTO accounts (client_token, segment, current_kdn, is_restructuring_active, created_at)
VALUES 
('22222222-3333-4444-5555-666666666666', 'RETAIL_CONSUMER', 0.44, false, NOW()),
('33333333-4444-5555-6666-777777777777', 'PRAGMATIC_AFFLUENT', 0.19, false, NOW())
ON CONFLICT (client_token) DO UPDATE 
SET current_kdn = EXCLUDED.current_kdn, segment = EXCLUDED.segment;

-- 2. client_profiles
INSERT INTO client_profiles (
    client_token, iin, full_name, age, gender, city, employment_type, industry,
    declared_income, archetype, stress_narrative, is_under_stalker_watch,
    current_risk_score, risk_level, created_at, updated_at
) VALUES 
(
    '22222222-3333-4444-5555-666666666666', '990812401923', 'Жанна Касымова', 27, 'FEMALE', 'Алматы',
    'OFFICIAL_EMPLOYED', 'Ритейл/Маркетинг', 420000.0, 'VULNERABLE',
    'Digital-маркетолог, SMM-лид. Высокая закредитованность BNPL (DTI 44%), 4 параллельные рассрочки, ночная тревожность в ДБО.',
    true, 0.168, 'YELLOW', NOW() - INTERVAL '180 days', NOW()
),
(
    '33333333-4444-5555-6666-777777777777', '940520301412', 'Санжар Муратов', 32, 'MALE', 'Атырау',
    'OFFICIAL_EMPLOYED', 'Нефтегазовый сектор / Производство', 850000.0, 'PRAGMATIC',
    'Главный инженер на производстве. Высокая платежная дисциплина, DTI 18.8%, скоринг ПКБ 0.76, стабильные выплаты в срок.',
    true, 0.048, 'GREEN', NOW() - INTERVAL '240 days', NOW()
)
ON CONFLICT (client_token) DO UPDATE 
SET full_name = EXCLUDED.full_name,
    declared_income = EXCLUDED.declared_income,
    current_risk_score = EXCLUDED.current_risk_score,
    risk_level = EXCLUDED.risk_level,
    updated_at = NOW();

-- 3. loans
INSERT INTO loans (
    loan_id, client_token, account_number, original_principal, current_principal_balance,
    interest_rate, effective_rate_gesv, monthly_payment, maturity_date,
    days_past_due, stage_ifrs9, status, updated_at
) VALUES 
(
    'bbbbbbbb-cccc-dddd-eeee-ffffffffffff', '22222222-3333-4444-5555-666666666666', 'KZ886010002003004002',
    2600000.00, 2600000.00, 0.22, 0.245, 185000.00, '2027-04-15', 0, 'STAGE_1', 'ACTIVE', NOW()
),
(
    'cccccccc-dddd-eeee-ffff-000000000000', '33333333-4444-5555-6666-777777777777', 'KZ886010002003004003',
    3800000.00, 3800000.00, 0.18, 0.198, 160000.00, '2027-11-20', 0, 'STAGE_1', 'ACTIVE', NOW()
)
ON CONFLICT (loan_id) DO UPDATE 
SET current_principal_balance = EXCLUDED.current_principal_balance,
    monthly_payment = EXCLUDED.monthly_payment,
    updated_at = NOW();

-- 4. scoring_events
INSERT INTO scoring_events (
    event_id, loan_id, p_default_30d, p_default_60d, model_version, shap_factors, feature_snapshot, triggered_at
) VALUES 
(
    'bbbbbbbb-cccc-dddd-eeee-222222222222', 'bbbbbbbb-cccc-dddd-eeee-ffffffffffff',
    0.168, 0.215, 'Full360CrossAttentionNet_v1.0',
    '[{"feature": "DTI_RATIO", "value": "44.0%", "impact": 0.38}, {"feature": "BNPL_ACTIVE", "value": "4 контракта", "impact": 0.29}, {"feature": "CARD_UTIL", "value": "82%", "impact": 0.25}]'::jsonb,
    '{"AMT_INCOME_TOTAL": 420000.0, "dti_ratio": 0.44, "EXT_SOURCE_2": 0.58, "pos_active_count": 4, "card_utilization": 0.82}'::jsonb,
    NOW()
),
(
    'cccccccc-dddd-eeee-ffff-333333333333', 'cccccccc-dddd-eeee-ffff-000000000000',
    0.048, 0.059, 'Full360CrossAttentionNet_v1.0',
    '[{"feature": "DTI_RATIO", "value": "18.8%", "impact": -0.25}, {"feature": "EXT_SOURCE_2", "value": "0.76", "impact": -0.28}, {"feature": "INST_AVG_DELAY", "value": "-1.5 дн.", "impact": -0.19}]'::jsonb,
    '{"AMT_INCOME_TOTAL": 850000.0, "dti_ratio": 0.188, "EXT_SOURCE_2": 0.76, "pos_completed_count": 3, "card_utilization": 0.12}'::jsonb,
    NOW()
)
ON CONFLICT (event_id) DO NOTHING;

-- 5. stalker_timeline_snapshots
INSERT INTO stalker_timeline_snapshots (
    snapshot_id, client_token, timestamp, risk_score, delta_pd, salary_trend, salary_delay_days,
    has_mfo_activity, active_bnpl_count, dti_estimate, daily_balance_7d, dbo_checks_count, primary_trigger
) VALUES 
(gen_random_uuid(), '22222222-3333-4444-5555-666666666666', NOW() - INTERVAL '15 days', 0.145, 0.02, 1.0, 0, false, 3, 0.41, 65000, 2, 'BNPL_CONTRACT_NEW'),
(gen_random_uuid(), '22222222-3333-4444-5555-666666666666', NOW(), 0.168, 0.023, 1.0, 2, false, 4, 0.44, 45000, 5, 'DBO_NIGHT_ANXIETY_SURGE'),
(gen_random_uuid(), '33333333-4444-5555-6666-777777777777', NOW() - INTERVAL '30 days', 0.052, -0.004, 1.0, 0, false, 0, 0.188, 380000, 0, 'SALARY_PAYROLL_INFLOW'),
(gen_random_uuid(), '33333333-4444-5555-6666-777777777777', NOW(), 0.048, -0.004, 1.05, 0, false, 0, 0.188, 420000, 0, 'BASE_STABLE_HEALTHY');
