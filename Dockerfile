FROM python:3.12.0b3-slim

WORKDIR /usr/src/app/

COPY TowerOfHanoiSolver/iterative/solver.py .

CMD ["python3", "solver.py", "-d", "4"]
