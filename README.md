# aitrade_site

<p>This is a Django website that allows user to register an account by linnking heir Binance account API to start trading cryptocurrency automatically.</p>
<p>The automated trading system uses the model trained from another repository (TradingBot).</p>
<p>The model uses deep reinforcement learning. PPO algorithm by OpenAI is used to stabilise the policy update.</p>
<p>The deep learning architecture is a CNN-LSTM model. CNN is used to extract features and create the relation of market information input. 
As CNN is highly sensitive, LSTM is implemented to indtroduce temporal delay. </p>


