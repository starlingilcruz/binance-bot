set -e

echo "Activating environment"

# source benv/bin/active

echo "Adding virtual environment to Jupyter Notebook"

# provides the IPython kernel for Jupyter
pip install ipykernel
python -m ipykernel install --name=benv

echo "Installing dependencies"

pip install -r requirements.txt
