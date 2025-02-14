<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
  xmlns="http://www.tei-c.org/ns/1.0"
  xmlns:ud="https://universaldependencies.org/u/feat"
  xmlns:tei="http://www.tei-c.org/ns/1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="1.0">

  <xsl:output method="xml"/>

  <!-- XPath 1.0 have lowercase function. I use a solution found here: https://stackoverflow.com/questions/28223036/converting-uppercase-to-lowercase-using-xslt-1-0-however-first-character-should. It uses the function 'translate', like this: 'translate($text, $uppercase, $lowercase)'. -->
  <xsl:variable name="upper" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
  <xsl:variable name="lower" select="'abcdefghijklmnopqrstuvwxyz'"/>

  <xsl:template match="tei:w">
    <xsl:copy>
      <xsl:choose>

        <!-- verbs -->
        <xsl:when test="@pos = 'VERB' or @pos = 'AUX'">
          <xsl:attribute name="msd">
            <xsl:choose>

              <!-- participes -->
              <xsl:when test="@ud:VerbForm = 'Part'">
                <xsl:text>p</xsl:text>
              </xsl:when>

              <!-- infinite -->
              <xsl:when test="@ud:VerbForm">
                <xsl:value-of select="translate(@ud:VerbForm, $upper, $lower)"/>
              </xsl:when>
            </xsl:choose>

            <!-- mood is abbreviated to a single letter -->
            <xsl:value-of select="translate(substring(@ud:Mood, 1, 1), $upper, $lower)"/>

            <!-- tense is abbreviated to three letters -->
            <xsl:value-of select="translate(substring(@ud:Tense, 1, 3), $upper, $lower)"/>
          </xsl:attribute>

          <!-- remove ud:* attributes -->
          <xsl:apply-templates select="@lemma | @pos | node()"/>
        </xsl:when>

        <!-- non-verbs: remove all attributes -->
        <xsl:otherwise>
          <xsl:apply-templates select="node()"/>
        </xsl:otherwise>

      </xsl:choose>
    </xsl:copy>
  </xsl:template>

  <!-- identity template -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
