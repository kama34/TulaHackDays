```
tmux new -s demo
```

```
conda activate zemfinder
```

```
cd /home/zemfinder
```

```
streamlit run app.py --server.port 8082
```

При следующем подключении через SSH можно будет вернуться к сессии tmux:
```
tmux attach -t demo
```
