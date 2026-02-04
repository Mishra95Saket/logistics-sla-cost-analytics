from __future__ import annotations
)


clf = LogisticRegression(max_iter=200, n_jobs=None)


pipe = Pipeline([("pre", pre), ("clf", clf)])
pipe.fit(X_train, y_train)


proba = pipe.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, proba)
ap = average_precision_score(y_test, proba)
brier = brier_score_loss(y_test, proba)


metrics = pd.DataFrame(
[{"roc_auc": float(auc), "avg_precision": float(ap), "brier": float(brier), "test_rows": int(len(y_test))}]
)
write_df(metrics, cfg.paths.reports_dir / f"model_delay_metrics.{fmt}", fmt)


# Score all shipments for ops triage
df_out = df[["shipment_id", "ship_date", "promised_date", "delivered_date", "on_time", "days_late"]].copy()
df_out["delay_risk_score"] = pipe.predict_proba(X)[:, 1]
df_out = df_out.sort_values("delay_risk_score", ascending=False)
write_df(df_out.head(5000), cfg.paths.reports_dir / f"top_delay_risk_shipments.{fmt}", fmt)


# SHAP explanation (small sample to keep runtime reasonable)
sample = X_test.sample(2000, random_state=cfg.random_seed)
# Explain the model in the transformed space
X_trans = pipe.named_steps["pre"].transform(sample)
explainer = shap.LinearExplainer(pipe.named_steps["clf"], X_trans)
shap_values = explainer(X_trans)


# Map transformed features back to names
ohe: OneHotEncoder = pipe.named_steps["pre"].named_transformers_["cat"]
cat_names = ohe.get_feature_names_out(cat_cols)
feature_names = list(cat_names) + num_cols


# Aggregate mean |SHAP| to rank features
mean_abs = np.abs(shap_values.values).mean(axis=0)
imp = pd.DataFrame({"feature": feature_names, "mean_abs_shap": mean_abs}).sort_values("mean_abs_shap", ascending=False)
write_df(imp.head(50), cfg.paths.reports_dir / f"model_delay_shap_top50.{fmt}", fmt)


print("✅ Delay-risk model complete. See model_delay_metrics and model_delay_shap_top50")




if __name__ == "__main__":
main()