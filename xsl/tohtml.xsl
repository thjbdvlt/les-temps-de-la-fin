<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
  xmlns="http://www.tei-c.org/ns/1.0"
  xmlns:ud="https://universaldependencies.org/u/feat"
  xmlns:tei="http://www.tei-c.org/ns/1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="1.0">

<xsl:output
  method="html"
  doctype-public="-//W3C//DTD HTML 4.0 Transitional//EN"/>

  <!-- XPath 1.0 have lowercase function. I use a solution found here: https://stackoverflow.com/questions/28223036/converting-uppercase-to-lowercase-using-xslt-1-0-however-first-character-should. It uses the function 'translate', like this: 'translate($text, $uppercase, $lowercase)'. -->
  <xsl:variable name="upper" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
  <xsl:variable name="lower" select="'abcdefghijklmnopqrstuvwxyz'"/>

  <!-- main html structure -->
  <xsl:template match="/">

    <html>
      <head>

        <!-- author -->
        <xsl:element name="meta">
          <xsl:attribute name="name">
            <xsl:text>author</xsl:text>
          </xsl:attribute>
          <xsl:attribute name="content">
            <xsl:text>Thibault Ziegler</xsl:text>
          </xsl:attribute>
        </xsl:element>

        <!-- description -->
        <xsl:element name="meta">
          <xsl:attribute name="description">
            <xsl:text>Édition électronique de La fin du monde de Camille Flammarion. Exporté de Wikisource. Annotations morphologiques des verbes par Thibault Ziegler.</xsl:text>
          </xsl:attribute>
        </xsl:element>

        <link rel="stylesheet" href="text.css"/>
        <link rel="stylesheet" href="svg.css"/>

      </head>
      <body>
        <nav>
          <ul>
            <li id="haut"><a href="#index">haut</a></li>
          </ul>
        </nav>
        <h1>Les temps verbaux de <i class="title">La fin du monde</i> <br/><span id="camille">(Camille Flammarion)</span></h1>
        <div id="index"></div>
        <div class="text">
          <xsl:apply-templates select="/tei:TEI/tei:text/tei:body/node()"/>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="tei:w">
    <xsl:choose>

      <!-- verbs and auxiliaries -->
      <xsl:when test="@pos = 'VERB' or @pos = 'AUX'">
        <xsl:element name="em">

          <!-- make the 'class' attribute -->
          <xsl:attribute name="class">
            <xsl:value-of select="@pos"/>
            <xsl:text> </xsl:text>
            <xsl:choose>
              <xsl:when test="@ud:VerbForm = 'Inf'">
                <xsl:text>f-inf</xsl:text>
              </xsl:when>
              <xsl:when test="@ud:VerbForm = 'Part'">
                <xsl:text>f-part </xsl:text>
                <xsl:text>t-</xsl:text>
                <xsl:value-of select="translate(@ud:Tense, $upper, $lower)"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:text>m-</xsl:text>
                <xsl:value-of select="translate(@ud:Mood, $upper, $lower)"/>
                <xsl:text> </xsl:text>
                <xsl:text>t-</xsl:text>
                <xsl:value-of select="translate(@ud:Tense, $upper, $lower)"/>
              </xsl:otherwise>
            </xsl:choose>

          </xsl:attribute>

          <!-- remove ud:* attributes -->
          <xsl:apply-templates select="node()"/>
        </xsl:element>
      </xsl:when>

      <!-- only keep text from non-verbs words -->
      <xsl:otherwise>
        <xsl:apply-templates select="text()"/>
      </xsl:otherwise>

    </xsl:choose>
  </xsl:template>

  <!-- only keep text from punctuation signs -->
  <xsl:template match="tei:pc">
    <xsl:apply-templates select="text()"/>
  </xsl:template>

  <!-- a div is a div -->
  <xsl:template match="tei:div">
    <xsl:element name="div">
      <xsl:attribute name="class">
        <xsl:value-of select="@type"/>
      </xsl:attribute>
      <xsl:apply-templates select="node()"/>
    </xsl:element>
  </xsl:template>

  <!-- TODO head -->
  <xsl:template match="tei:head">
    <xsl:choose>
      <xsl:when test="../@type='part'">
        <h2>
          <xsl:value-of select="text()"/>
        </h2>
      </xsl:when>
      <xsl:when test="../@type='chapter'">
        <h3>
          <xsl:value-of select="text()"/>
        </h3>
      </xsl:when>
      <xsl:otherwise>
        <h4>
          <xsl:value-of select="text()"/>
        </h4>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- paragraphs are kept as-is (they have no attributes) -->
  <xsl:template match="tei:p">
    <xsl:copy>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- sentences are removed, their content is kept -->
  <xsl:template match="tei:s">
    <xsl:apply-templates select="node()"/>
  </xsl:template>

  <!-- title -->
  <xsl:template match="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title" name="title">
    <xsl:copy>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- q element is mainly use for dialogs -->
  <xsl:template match="tei:q">
    <xsl:copy>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="tei:blockquote">
    <xsl:copy>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- remove date and measure elements -->
  <!-- TODO: make spans -->
  <xsl:template match="tei:date">
      <xsl:apply-templates select="node()"/>
  </xsl:template>
  <xsl:template match="tei:measure">
      <xsl:apply-templates select="node()"/>
  </xsl:template>

</xsl:stylesheet>
