#!/bin/bash
# 35_buildstory.sh -- write the ledger entry that the STANDING RULE demands at
# EVERY ship AND EVERY reject.  Two files, one call, no hand-editing.
#
#   usage: [DOC=docs/strategy/<file>.md] [TITLE="..."] \
#          bash S/pipeline/35_buildstory.sh <LABEL> "<one-line verdict>"
#
#   ... and the PROSE paragraph(s) on stdin, which is where the story goes:
#
#       bash S/pipeline/35_buildstory.sh GEESE1 "HARD REJECT ..." <<'EOF'
#       Then we counted our own birds, and the invitation evaporated. ...
#       EOF
#
# With nothing on stdin the verdict line is used as the paragraph and the entry
# is a stub -- honest, but a stub.  BUILD-STORY.md is read by a human later; a
# one-line entry is what makes an axis get re-explored.
#
# WHAT IT WRITES
#   docs/strategy/BUILD-STORY.md   `## <LABEL> — <title>` + a blank line + the
#                                  paragraph(s), appended at the end, in the
#                                  format every entry from BUILDSTORY38 on uses.
#   S/buildstory/index.tsv         ONE row, `<doc>.md<TAB><verdict>`, two columns
#                                  and a literal tab -- the index is read with
#                                  `cut -f1,2` and a second tab breaks it.
#
# WHY A SCRIPT.  The rule ("BUILD-STORY at every ship and every reject") has been
# in the operator manual since the ESR ship and is still the step most often
# skipped, because it is the one step with no number attached.  A rejected axis
# that is not written down gets re-explored by the next agent -- MELONGENES1 and
# GEESE1 both re-priced a family an earlier doc had already closed.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
LABEL=$1; VERDICT=$2
[ -n "$LABEL" ] && [ -n "$VERDICT" ] \
  || die "usage: bash S/pipeline/35_buildstory.sh <LABEL> \"<one-line verdict>\"  (prose on stdin)"

BS=$R/docs/strategy/BUILD-STORY.md
IX=$R/S/buildstory/index.tsv
[ -s "$BS" ] || die "no $BS"
mkdir -p "$(dirname $IX)"

slug=$(echo "$LABEL" | tr 'A-Z' 'a-z' | tr -cd 'a-z0-9-')
DOC=${DOC:-docs/strategy/$(date -u +%F)-$slug.md}
case "$DOC" in /*) DOCREL=${DOC#$R/} ;; *) DOCREL=$DOC ;; esac
DOCBASE=$(basename "$DOCREL")
TITLE=${TITLE:-$(echo "$VERDICT" | cut -c1-90)}

# A tab in the verdict would make the index a three-column file.
VERDICT=$(printf '%s' "$VERDICT" | tr '\t\n' '  ')

grep -q "^## $LABEL " "$BS" && say "NOTE: BUILD-STORY.md already carries a '## $LABEL' heading -- appending a second one"
grep -q "^$DOCBASE	" "$IX" 2>/dev/null && die "$DOCBASE already has an index row -- edit it, do not double it"
[ -s "$R/$DOCREL" ] || say "NOTE: $DOCREL does not exist yet.  The index points at it; write it."

# stdin only when it is not a terminal and not empty
BODY=""
if [ ! -t 0 ]; then BODY=$(cat); fi
[ -n "$BODY" ] || { BODY="$VERDICT"; say "NOTE: nothing on stdin -- the entry is a ONE-LINE STUB"; }

{ echo; echo "## $LABEL — $TITLE"; echo; echo "$BODY"; } >> "$BS"
printf '%s\t%s\n' "$DOCBASE" "$VERDICT" >> "$IX"

say "BUILD-STORY.md += '## $LABEL — $TITLE' ($(printf '%s' "$BODY" | wc -w) words)"
say "index.tsv      += $DOCBASE  ($(printf '%s' "$VERDICT" | wc -c) chars)"
echo
tail -4 "$BS"
echo "---"
cut -c1-120 <<<"$(tail -1 $IX)"
next "git add docs/strategy/BUILD-STORY.md S/buildstory/index.tsv $DOCREL && git commit"
