```
tmux new -s demo_v2.0
```

```
conda activate zemfinder
```

```
cd /home/zemfinder
```

```
streamlit run app_v2.0.py --server.port 8083
```

При следующем подключении через SSH можно будет вернуться к сессии tmux:
```
tmux attach -t demo_v2.0
```
