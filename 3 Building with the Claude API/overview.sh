cat overview.md | grep ^# | grep -oPn ' (.*)' | sed -e 's/://' | xargs -I {} mkdir -p {}

cat overview.md | awk 'if($0 ~ /^# /) {print "mkdir -p \"" substr($0, 3) "\""} else {print "touch \"" substr($0, 4) "\".md"}' | sh