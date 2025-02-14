<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
  xmlns="http://www.tei-c.org/ns/1.0"
  xmlns:ud="https://universaldependencies.org/u/feat"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="1.0">

  <xsl:output method="xml"/>

  <xsl:template match="tei:w">
    <xsl:copy>
      <xsl:attribute name="msd">
        <!-- i do not use @ud:*, because it needs to be sorted. -->
        <xsl:value-of select="@ud:VerbForm"/>
        <xsl:value-of select="@ud:PronType"/>
        <xsl:value-of select="@ud:Definite"/>
        <xsl:value-of select="@ud:NumType"/>
        <xsl:value-of select="@ud:Mood"/>
        <xsl:value-of select="@ud:Tense"/>
        <xsl:value-of select="@ud:Person"/>
        <xsl:value-of select="@ud:Number"/>
        <xsl:value-of select="@ud:Number_psor"/>
        <xsl:value-of select="@ud:Voice"/>
        <xsl:value-of select="@ud:Polarity"/>
        <xsl:if test="@ud:Poss">
          <xsl:text>Poss</xsl:text>
        </xsl:if>
        <xsl:if test="@ud:Reflex">
          <xsl:text>Reflex</xsl:text>
        </xsl:if>
      </xsl:attribute>
      <!-- all attributes under 'ud' namespace are removed. -->
      <xsl:apply-templates select="@lemma | @pos | node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
