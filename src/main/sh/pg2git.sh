#!/bin/sh

infile="$1"
if [ \! -s "$infile" ]; then
	echo Missing infile argument, aborting.
	exit 1
fi

script_dir=$(dirname "$0")
dir_name=../../..
base_dir="$script_dir/$dir_name"
wiki_sub_dir="src/main/wiki"
adoc_sub_dir="src/main/adoc"
work_subdir="target/work"
ns=http://www.mediawiki.org/xml/export-0.6/

page_title=$( xmlstarlet sel -T -N w=$ns \
	-t -m "//w:page" -v "w:title" \
	"$infile" )
revisions=($( xmlstarlet sel -T -N w=$ns \
		-t -m '//w:revision' -v 'w:id' --nl \
		"$infile" ))

echo Found ${#revisions[@]} revisions

mkdir -p "$base_dir/$wiki_sub_dir"
wiki_page_path="$base_dir/$wiki_sub_dir/${page_title}.wiki"
mkdir -p "$base_dir/$adoc_sub_dir"
adoc_page_path="$base_dir/$adoc_sub_dir/${page_title}.adoc"
work_dir="$base_dir/$work_subdir/$page_title"
mkdir -p "$work_dir"
git checkout master
git reset --hard start
git branch -D wikia/pages
git branch -D wikia/images
git branch -D adoc
git gc
git branch wikia/pages
git branch wikia/images
git branch adoc
for revision in ${revisions[@]}; do
	git checkout wikia/pages
	xmlstarlet sel -T -N w=$ns -E utf-8 \
		-t -m "//w:revision[w:id='$revision']" -v 'w:text' \
		"$infile" > "$wiki_page_path"
	timestamp=$( xmlstarlet sel -T -N w=$ns \
		-t -m "//w:revision[w:id='$revision']" -v 'w:timestamp' \
		"$infile" )
	comment=$( xmlstarlet sel -T -N w=$ns \
		-t -m "//w:revision[w:id='$revision']" -v 'w:comment' \
		"$infile" |
		perl -pe 's#/\*\s+(.*)\s+\*?/#(\1):#g' )
	echo "$revision - $timestamp : $comment"
	git add "$wiki_page_path"
	git commit --date="$timestamp" -m "$comment"
	git log -n 1
	#cp "$wiki_page_path" "$work_dir"
	git checkout adoc
	git merge --no-commit wikia/pages
	perl -pe '
		s:^'"'''"'(.*?)'"'''"'<br.*?/>$:$1\n:; # fix hardcoded document title
		s:^<h2.*?>(.*?)</h2>$:==$1==:; # fix hardcoded heading
		s:^=(.*)=$:$1:; # promote all headers
		s:^<div\s+style="page-break-after\:\s+always"></div>$:\n>> PAGEBREAK HERE <<\n:; # remember hardcoded page break
		s:<s>(.*?)</s>:%%s%$1%/s%%:g; # remember strike-through
		s:(?<!'\'')'\''([^ '\'']+?)'\''(?!'\''):%%'\''%$1%'\''%%:g; # remember single quoted words
		s#[\|\!](:?(r)ow|(c)ol)span="(\d+)".*?\|#$&%%$2$3$4%%#g; # remember colspan/rowspan
		s:<br>:%%br%%:g; # remember line breaks
		s:&beta;:%%beta%%:g; # remember beta character
		s:\|thumb\]\]:$&%%thumb%%:g; # remember thumb images
	' "$wiki_page_path" | \
	pandoc -f mediawiki -t asciidoc --toc | \
		perl -pe 'BEGIN {
			use utf8;
			use Text::Unidecode;
			use Encode "decode";
			}
			($. == 1) and s{$}{
=======
Arnauld Van Muysewinkel <arnauldvm\@gmail.com>'"
:revnumber: W$revision
:revdate: ${timestamp:0:10}
//:revremark: $comment"'
:doctype: article
:lang: fr
:encoding: utf8
:toc:
:toc-placement: manual
:toclevels: 4
:toc-title: Contenu
//:numbered:
:imagesdir: ../img
:data-uri:
:br: pass:[<br>]
:beta: pass:[&beta;]
};
			s/>> PAGEBREAK HERE <</<<<\ntoc::[]\n<<</; # fix hardcoded page break
			s/^\[\[.*?\]\]$/unidecode(decode "UTF-8", $&)/e; # fix identifiers with accents
			s:%%s%(.*?)%/s%%:[line-through]#$1#:g; # fix strike-through
			s:%%'\''%([^ '\'']+?)%'\''%%:\\'\''$1'\'':g; # fix single quoted words
			s:\|%%c(\d+)%%:$1+|:g; # fix colspan
			s:\|%%r(\d+)%%:.$1+|:g; # fix rowspan
			s:%%br%%:{br}:g; # fix line breaks
			s:%%beta%%:{beta}:g; # fix beta character
			s/(image:.*?\[)(.*?),/\1"\2",/g; # fix images alt attribute
			s:\]%%thumb%%:,width=180]:g; # fix thumb images
		' > "$adoc_page_path"
	git add "$adoc_page_path"
	git commit --date="$timestamp" -m "convert: $comment"
	git log -n 1
done
git checkout master
git merge --no-edit adoc

src/main/sh/img2git.sh -p ${page_title}

asciidoc $adoc_page_path

