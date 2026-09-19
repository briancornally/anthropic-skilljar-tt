rm -v */.envrc
DIRS=($(ls */*.ipynb | awk -F/ '{print $1}' | sort -u))
for f in ${DIRS[@]}; do pushd $f; ln -s ../.envrc .; direnv allow; popd; done

IPYNB_NOTBOOKS=($(find . -name "*.ipynb"))
for f in ${IPYNB_NOTBOOKS[@]}; do
  yq -i -p=json -o=json '
    .metadata.kernelspec = {
      "display_name": "Python 3 (ipykernel)",
      "language": "python",
      "name": "python3"
    } |
    .metadata.language_info = {
      "codemirror_mode": {"name": "ipython", "version": 3},
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.14.7"
    }
  ' "$f"
done

for f in ${DIRS[@]}; do code $f; done
code */*.ipynb

rm -rf /Users/brian/venv/
mkdir -p /Users/brian/venv/
rm -rf $UV_PROJECT_ENVIRONMENT
uv sync
jupyter kernelspec list