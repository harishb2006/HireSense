from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from typing import Dict, Any
import io

class PDFScorecard:
    """
    Generate professional PDF scorecards for resume analysis and interview performance
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f2937'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ))
        
        # Section header
        if 'SectionHeader' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHeader',
                parent=self.styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#2563eb'),
                spaceAfter=12,
                spaceBefore=20,
                fontName='Helvetica-Bold'
            ))
        
        # Body text
        if 'BodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='BodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#374151'),
                spaceAfter=10,
                alignment=TA_JUSTIFY
            ))
        
        # Bullet points
        if 'BulletPoint' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='BulletPoint',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#4b5563'),
                leftIndent=20,
                spaceAfter=8
            ))
    
    def generate_full_scorecard(
        self,
        analysis: Dict[str, Any],
        interview_summary: Dict[str, Any] = None,
        candidate_name: str = "Candidate"
    ) -> bytes:
        """
        Generate comprehensive PDF scorecard with analysis and interview results
        """
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        
        # Header
        story.append(Paragraph("HireSense", self.styles['CustomTitle']))
        story.append(Paragraph("Job Readiness Scorecard", self.styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        # Metadata table
        metadata = [
            ["Candidate:", candidate_name],
            ["Date:", datetime.now().strftime("%B %d, %Y")],
            ["Report Type:", "Resume Analysis & Interview Performance"]
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#6b7280')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(metadata_table)
        story.append(Spacer(1, 0.3*inch))
        
        # === RESUME ANALYSIS SECTION ===
        story.append(Paragraph("📊 Resume Analysis", self.styles['SectionHeader']))
        
        # Match Score Box
        match_score = analysis.get('match_score', 0)
        score_color = self._get_score_color(match_score)
        score_label = self._get_score_label(match_score)
        
        score_data = [[
            Paragraph(f"<b>{match_score}%</b>", self.styles['Heading1']),
            Paragraph(f"<b>{score_label}</b><br/>{analysis.get('overall_assessment', '')[:200]}...", 
                     self.styles['BodyText'])
        ]]
        
        score_table = Table(score_data, colWidths=[1.5*inch, 4.5*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), score_color),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#f9fafb')),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 36),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#e5e7eb')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Why Not Passing
        why_not_passing = analysis.get('why_not_passing', {})
        if why_not_passing.get('main_reasons'):
            story.append(Paragraph("⚠️ Key Issues", self.styles['SectionHeader']))
            for idx, reason in enumerate(why_not_passing['main_reasons'][:3], 1):
                story.append(Paragraph(f"<b>{idx}.</b> {reason}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.15*inch))
        
        # Missing Keywords
        missing_keywords = analysis.get('missing_keywords', [])
        if missing_keywords:
            story.append(Paragraph("🔑 Missing Critical Skills", self.styles['SectionHeader']))
            
            keyword_data = [['Skill', 'Importance', 'Why It Matters']]
            for kw in missing_keywords[:5]:
                keyword_data.append([
                    kw.get('keyword', ''),
                    kw.get('importance', '').upper(),
                    kw.get('why_matters', '')[:100] + '...'
                ])
            
            keyword_table = Table(keyword_data, colWidths=[1.5*inch, 1*inch, 3.5*inch])
            keyword_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(keyword_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Actionable Steps
        actionable_steps = analysis.get('actionable_next_steps', [])
        if actionable_steps:
            story.append(Paragraph("✅ Recommended Actions", self.styles['SectionHeader']))
            for idx, step in enumerate(actionable_steps[:5], 1):
                story.append(Paragraph(f"<b>{idx}.</b> {step}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.2*inch))
        
        # === INTERVIEW PERFORMANCE (if available) ===
        if interview_summary:
            story.append(PageBreak())
            story.append(Paragraph("🎤 Interview Performance", self.styles['SectionHeader']))
            
            # Overall Interview Score
            interview_score = interview_summary.get('overall_score', 0)
            perf_level = interview_summary.get('performance_level', 'N/A')
            
            interview_score_data = [[
                Paragraph(f"<b>{interview_score}%</b>", self.styles['Heading1']),
                Paragraph(f"<b>Performance Level: {perf_level}</b><br/>Mock interview completed with detailed feedback", 
                         self.styles['BodyText'])
            ]]
            
            interview_table = Table(interview_score_data, colWidths=[1.5*inch, 4.5*inch])
            interview_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), self._get_score_color(interview_score)),
                ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#f0f9ff')),
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 36),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
                ('PADDING', (0, 0), (-1, -1), 12),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#e5e7eb')),
            ]))
            story.append(interview_table)
            story.append(Spacer(1, 0.2*inch))
            
            # Strengths
            strengths = interview_summary.get('strengths', [])
            if strengths:
                story.append(Paragraph("💪 Strengths Demonstrated", self.styles['SectionHeader']))
                for strength in strengths[:3]:
                    story.append(Paragraph(f"• {strength}", self.styles['BulletPoint']))
                story.append(Spacer(1, 0.15*inch))
            
            # Areas for Improvement
            improvements = interview_summary.get('improvements', [])
            if improvements:
                story.append(Paragraph("📈 Areas for Improvement", self.styles['SectionHeader']))
                for improvement in improvements[:3]:
                    story.append(Paragraph(f"• {improvement}", self.styles['BulletPoint']))
                story.append(Spacer(1, 0.15*inch))
            
            # Next Steps
            next_steps = interview_summary.get('next_steps', [])
            if next_steps:
                story.append(Paragraph("🎯 Next Steps", self.styles['SectionHeader']))
                for idx, step in enumerate(next_steps[:4], 1):
                    story.append(Paragraph(f"<b>{idx}.</b> {step}", self.styles['BulletPoint']))
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            f"<i>Generated by HireSense AI • {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>",
            self.styles['Normal']
        ))
        
        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _get_score_color(self, score: int) -> colors.Color:
        """Get color based on score"""
        if score >= 70:
            return colors.HexColor('#10b981')  # Green
        elif score >= 50:
            return colors.HexColor('#f59e0b')  # Orange
        else:
            return colors.HexColor('#ef4444')  # Red
    
    def _get_score_label(self, score: int) -> str:
        """Get label based on score"""
        if score >= 70:
            return "Good Match"
        elif score >= 50:
            return "Moderate Match"
        else:
            return "Needs Improvement"
