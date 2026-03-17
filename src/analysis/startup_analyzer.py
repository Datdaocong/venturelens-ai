import pandas as pd

class StartupAnalyzer:

    def __init__(self, df):
        self.df = df

    def calculate_score(self):

        self.df["startup_score"] = (
            self.df["product_score"] * 0.3 +
            self.df["team_score"] * 0.25 +
            self.df["traction_score"] * 0.25 +
            self.df["innovation_score"] * 0.2
        )

        return self.df

    def rank_startups(self):

        df_ranked = self.df.sort_values(
            by="startup_score",
            ascending=False
        )

        return df_ranked

    def get_startup(self, name):

        return self.df[self.df["startup_name"] == name]
    def investment_signal(self):

        def signal(score):

            if score >= 8:
                return "STRONG INVEST"

            elif score >= 6:
                return "WATCHLIST"

            else:
                return "PASS"

        self.df["signal"] = self.df["startup_score"].apply(signal)

        return self.df
    
    def generate_analysis(self, startup_row):

        score = startup_row["startup_score"]
        signal = startup_row["signal"]

        if signal == "STRONG INVEST":
            verdict = "This startup shows strong fundamentals and is a promising investment opportunity."

        elif signal == "WATCHLIST":
            verdict = "This startup has potential but requires further monitoring before investment."

        else:
            verdict = "This startup currently does not meet investment criteria."

        analysis = f"""
        **Startup:** {startup_row['startup_name']}

        **Overall Score:** {score:.2f}

        **Investment Signal:** {signal}

        **Product Strength:** {startup_row['product_score']:.2f}  
        **Team Strength:** {startup_row['team_score']:.2f}  
        **Traction:** {startup_row['traction_score']:.2f}  
        **Innovation:** {startup_row['innovation_score']:.2f}

        **Verdict:** {verdict}
        """

        return analysis