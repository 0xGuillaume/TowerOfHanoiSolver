FROM python:latest

WORKDIR /usr/src/app/

COPY TowerOfHanoiSolver/iterative/solver.py .

CMD ["python3", "solver.py", "-d", "4"]
