#!/bin/sh

infile="$1"

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
git branch wiki
git branch adoc
for revision in ${revisions[@]}; do
	git checkout wiki
	xmlstarlet sel -T -N w=$ns -E utf-8 \
		-t -m "//w:revision[w:id='$revision']" -v 'w:text' \
		"$infile" | \
		perl -pe '
			s:^'"'''"'(.*?)'"'''"'<br.*?/>$:$1\n:; # fix hardcoded document title
			s:^<h2.*?>(.*?)</h2>$:==$1==:; # fix hardcoded heading
			s:^=(.*)=$:$1:; # promote all headers
			s:^<div\s+style="page-break-after\:\s+always"></div>$:\n>> PAGEBREAK HERE <<\n:; # remember hardcoded page break
			s:<s>(.*?)</s>:>>s<<$1>>/s<<:g; # remember strike-through
		' > "$wiki_page_path"
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
	git merge --no-commit wiki
	#pandoc -f mediawiki -t asciidoc -o "$adoc_page_path" "$work_dir/${page_title}.wiki"
	pandoc -f mediawiki -t asciidoc --toc "$wiki_page_path" | \
		perl -pe 'BEGIN {
			use utf8;
			use Text::Unidecode;
			use Encode "decode";
			}
			($. == 1) and s{$}{
=======
Arnauld Van Muysewinkel <arnauldvm@gmail.com>'"
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
:numbered:
};
			s/>> PAGEBREAK HERE <</<<<\ntoc::[]\n<<</; # fix hardcoded page break
			s/^\[\[.*?\]\]$/unidecode(decode "UTF-8", $&)/e; # fix identifiers with accents
			s:>>s<<(.*?)>>/s<<:[line-through]#$1#:g; # fix strike-through
			s/image:/image:img\//g; # images in a subfolder
		' > "$adoc_page_path"
	git add "$adoc_page_path"
	git commit --date="$timestamp" -m "convert: $comment"
	git log -n 1
done
git checkout master
git merge --no-edit adoc

asciidoc $adoc_page_path
