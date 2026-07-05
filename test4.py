from prediction.risk_reward import RiskRewardEngine

engine = RiskRewardEngine()

result = engine.run(

    trade_type="SELL ON RISE",

    current_price=23865.75,

    entry_low=24140.87,

    entry_high=24189.25,

    stop_loss=24310.20,

    target1=23784.95,

    target2=23536.75

)

print(result)