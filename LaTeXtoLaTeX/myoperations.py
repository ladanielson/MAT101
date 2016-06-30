
import re

import utilities
import component

def setvariables(text):

    component.chapter_abbrev = utilities.argument_of_macro(text,"chap",2)


###################

def mytransform(text):

    thetext = text

    # replace \begin{prop}{the_label} by
    # \begin{prop}\label{proposition:chaptername:the_label}
    thetext = utilities.replacemacro(thetext,r"\begin{prop}",1,
                         r"\begin{prop}\label{proposition:"+component.chapter_abbrev+":#1}")

    # and similarly for example and exercise (yes, this can be in a loop)
    thetext = utilities.replacemacro(thetext,r"\begin{example}",1,
                         r"\begin{example}\label{example:"+component.chapter_abbrev+":#1}")
    thetext = utilities.replacemacro(thetext,r"\begin{exercise}",1,
                         r"\begin{exercise}\label{exercise:"+component.chapter_abbrev+":#1}")

    # in actions.tex and crypt.tex many examples start with something like
    # \noindent {\bf Example 2.}
    # and end with
    # \hspace{\fill} $\blacksquare$
    # so we convert these to \begin{example} \end{example}.
    # Labels and references still need to be added by hand.

    thetext = re.sub(r"\\noindent\s*{\\bf\s+Example\s+[0-9.]+\s*}",r"\\begin{example}",thetext)
    thetext = re.sub(r"\\hspace{\\fill}\s*\$\\blacksquare\$",r"\\end{example}",thetext)

    # delete empty label arguments
    thetext = re.sub(r"\\label{[a-zA-Z]+:[a-zA-Z]+:}","",thetext)

    return thetext

#######################

def transformMAT101(text):

    thetext = text

    # lower case the hN tags
    thetext = re.sub("H([1-9])>",r"h\1>",thetext)

    # delete tags we don't want
    thetext = re.sub(r"<center>\s*","", thetext)
    thetext = re.sub(r"</center>\s*","", thetext)
    thetext = re.sub(r"</?\s?br\s?/?>","", thetext)
    thetext = re.sub(r"<font\s+color=#[0-9A-F]+><u>","", thetext)
    thetext = re.sub(r"</u></font>","", thetext)
    thetext = re.sub(r"<font\s+color=#[0-9A-F]+>","", thetext)
    thetext = re.sub(r"</font>","", thetext)

    # delete everything before <body>
    thetext = re.sub(r".*<body>","<chapter>", thetext,0, re.DOTALL)
    thetext = re.sub(r"</body>.*","", thetext,0, re.DOTALL)
    thetext = re.sub(r"\s*<h1>","\n<title>", thetext)
    thetext = re.sub(r"</h1>\s*","</title>\n", thetext)

    thetext = re.sub(r"<h3>Objectives:</h3>\s*<ul>\s*(.*?)</ul>","<objectives>\n<ul>\n" + r"\1" + "</ul>\n</objectives>", thetext,0, re.DOTALL)

    # add the closing section tags, then convert h2 to section/title
    thetext = re.sub(r"<h2>","</section>\n<h2>",thetext)
    thetext = re.sub(r"</section>","",thetext,1)
    thetext += "</section>"
    thetext = re.sub(r"<h2>(.*?)</h2>","<section>\n<title>" + r"\1" + "</title>\n",thetext)

    # add the closing example tags, per section
    thetext = re.sub(r"<h3>Example","</example>\n<h3>Example",thetext)
    thetext = re.sub(r"</section>","</example>\n</section>",thetext)
    thetext = re.sub(r"(<section>.*?)</example>",r"\1",thetext,0,re.DOTALL)
    # then convert <h3>Example to example/title tags
    thetext = re.sub(r"<h3>Example.*?:(.*?)</h3>","<example>\n<title>" + r"\1" + "</title>\n",thetext)
    
    thetext = re.sub(r"(<example>.*?</title>)(.*?)<table",r"\1\n<p>\2</p>\n<table",thetext,0,re.DOTALL)
    

    thetext = re.sub(r"\\\(","<m>",thetext)
    thetext = re.sub(r"\\\)","</m>",thetext)

    thetext = re.sub(r"<img ([^>]+?)\s*/>",r"<image \1 />",thetext)
    thetext = re.sub(r"<img ([^>]+?)\s*>",r"<image \1 />",thetext)
    thetext = re.sub(r"src=",r"source=",thetext)

    thetext = re.sub(r"&gt;",r"<gt />",thetext)
    thetext = re.sub(r"&lt;",r"<lt />",thetext)
    thetext = re.sub(r"&gt ",r"<gt />",thetext)
    thetext = re.sub(r"&lt ",r"<lt />",thetext)

    thetext = re.sub(r"&",r"<amp />",thetext)

#    thetext = re.sub(r"\\%","<percent />",thetext)

    # improve some spacing

    thetext = re.sub(r"\s*<td","\n    <td",thetext)
    thetext = re.sub(r"\s*</td>\s*","</td>\n",thetext)
    thetext = re.sub(r"\s*<tr>\s*","\n  <tr>\n",thetext)
    thetext = re.sub(r"\s*</tr>\s*","\n  </tr>\n",thetext)

    thetext = re.sub(r"\s*<section","\n\n<section",thetext)
    thetext = re.sub(r"\s*<example","\n\n<example",thetext)

    thetext += "\n</chapter>"

    return thetext

