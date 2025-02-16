<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
  xmlns="http://www.tei-c.org/ns/1.0"
  xmlns:tei="http://www.tei-c.org/ns/1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="1.0">

  <xsl:output method="xml"/>

  <!-- remove s/measure/date elements, keep their contents -->
  <xsl:template match="tei:s">
      <xsl:apply-templates select="node()"/>
  </xsl:template>

  <!-- identity template -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
