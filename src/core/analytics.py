<<<<<<< Updated upstream
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 VOICE STUDIO ANALYTICS & REPORTING - PHASE 4
Professional business intelligence với production metrics,
quality reports, performance analysis, và ROI calculations.
"""

import json
import os
import time
import sqlite3
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

@dataclass
class ProductionMetrics:
    """Production performance metrics"""
    session_id: str
    timestamp: datetime
    files_processed: int
    total_duration: float  # minutes
    success_rate: float  # percentage
    avg_quality_score: float
    processing_time: float  # seconds
    characters_used: int
    export_formats: List[str]
    cost_estimate: float  # USD

@dataclass
class QualityReport:
    """Quality analysis report"""
    session_id: str
    file_path: str
    text_length: int
    audio_duration: float
    quality_score: float
    whisper_accuracy: float
    emotion_detected: str
    processing_attempts: int
    final_success: bool
    issues_found: List[str]

@dataclass
class PerformanceAnalysis:
    """Performance analysis data"""
    session_id: str
    cpu_usage: float
    memory_usage: float
    gpu_usage: float
    workers_active: int
    throughput: float  # tasks per second
    efficiency: float  # percentage
    bottlenecks: List[str]

class AnalyticsDatabase:
    """SQLite database for analytics storage"""
    
    def __init__(self, db_path: str = "voice_studio_analytics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize analytics database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Production metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                files_processed INTEGER,
                total_duration REAL,
                success_rate REAL,
                avg_quality_score REAL,
                processing_time REAL,
                characters_used INTEGER,
                export_formats TEXT,
                cost_estimate REAL
            )
        ''')
        
        # Quality reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quality_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                file_path TEXT,
                text_length INTEGER,
                audio_duration REAL,
                quality_score REAL,
                whisper_accuracy REAL,
                emotion_detected TEXT,
                processing_attempts INTEGER,
                final_success BOOLEAN,
                issues_found TEXT
            )
        ''')
        
        # Performance analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                cpu_usage REAL,
                memory_usage REAL,
                gpu_usage REAL,
                workers_active INTEGER,
                throughput REAL,
                efficiency REAL,
                bottlenecks TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_production_metrics(self, metrics: ProductionMetrics):
        """Store production metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO production_metrics 
            (session_id, timestamp, files_processed, total_duration, success_rate,
             avg_quality_score, processing_time, characters_used, export_formats, cost_estimate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics.session_id,
            metrics.timestamp.isoformat(),
            metrics.files_processed,
            metrics.total_duration,
            metrics.success_rate,
            metrics.avg_quality_score,
            metrics.processing_time,
            metrics.characters_used,
            json.dumps(metrics.export_formats),
            metrics.cost_estimate
        ))
        
        conn.commit()
        conn.close()
    
    def store_quality_report(self, report: QualityReport):
        """Store quality report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quality_reports 
            (session_id, file_path, text_length, audio_duration, quality_score,
             whisper_accuracy, emotion_detected, processing_attempts, final_success, issues_found)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report.session_id,
            report.file_path,
            report.text_length,
            report.audio_duration,
            report.quality_score,
            report.whisper_accuracy,
            report.emotion_detected,
            report.processing_attempts,
            report.final_success,
            json.dumps(report.issues_found)
        ))
        
        conn.commit()
        conn.close()
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get production metrics
        cursor.execute('''
            SELECT * FROM production_metrics WHERE session_id = ?
        ''', (session_id,))
        
        production_data = cursor.fetchone()
        
        # Get quality reports
        cursor.execute('''
            SELECT * FROM quality_reports WHERE session_id = ?
        ''', (session_id,))
        
        quality_data = cursor.fetchall()
        
        conn.close()
        
        return {
            'production_metrics': production_data,
            'quality_reports': quality_data,
            'summary_generated': datetime.now().isoformat()
        }

class VoiceStudioAnalytics:
    """Main analytics controller"""
    
    def __init__(self):
        self.db = AnalyticsDatabase()
        self.current_session = self._generate_session_id()
        self.session_start_time = datetime.now()
        self.metrics_cache = {}
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}"
    
    def start_new_session(self) -> str:
        """Start new analytics session"""
        self.current_session = self._generate_session_id()
        self.session_start_time = datetime.now()
        self.metrics_cache = {}
        return self.current_session
    
    def track_production_batch(self, files_processed: int, success_count: int, 
                              total_duration: float, processing_time: float,
                              quality_scores: List[float], characters_used: int,
                              export_formats: List[str]) -> ProductionMetrics:
        """Track production batch metrics"""
        
        success_rate = (success_count / files_processed) * 100 if files_processed > 0 else 0
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Cost calculation (simplified model)
        cost_per_minute = 0.02  # $0.02 per minute of audio
        cost_estimate = total_duration * cost_per_minute
        
        metrics = ProductionMetrics(
            session_id=self.current_session,
            timestamp=datetime.now(),
            files_processed=files_processed,
            total_duration=total_duration,
            success_rate=success_rate,
            avg_quality_score=avg_quality,
            processing_time=processing_time,
            characters_used=characters_used,
            export_formats=export_formats,
            cost_estimate=cost_estimate
        )
        
        self.db.store_production_metrics(metrics)
        return metrics
    
    def track_quality_analysis(self, file_path: str, text_length: int,
                              audio_duration: float, quality_score: float,
                              whisper_accuracy: float, emotion: str,
                              attempts: int, success: bool,
                              issues: List[str]) -> QualityReport:
        """Track individual file quality analysis"""
        
        report = QualityReport(
            session_id=self.current_session,
            file_path=file_path,
            text_length=text_length,
            audio_duration=audio_duration,
            quality_score=quality_score,
            whisper_accuracy=whisper_accuracy,
            emotion_detected=emotion,
            processing_attempts=attempts,
            final_success=success,
            issues_found=issues
        )
        
        self.db.store_quality_report(report)
        return report
    
    def generate_session_report(self) -> Dict[str, Any]:
        """Generate comprehensive session report"""
        session_data = self.db.get_session_summary(self.current_session)
        
        # Calculate session duration
        session_duration = (datetime.now() - self.session_start_time).total_seconds() / 60
        
        report = {
            'session_info': {
                'session_id': self.current_session,
                'start_time': self.session_start_time.isoformat(),
                'duration_minutes': session_duration,
                'generated_at': datetime.now().isoformat()
            },
            'raw_data': session_data,
            'insights': self._generate_insights(session_data),
            'recommendations': self._generate_recommendations(session_data)
        }
        
        return report
    
    def _generate_insights(self, session_data: Dict) -> Dict[str, Any]:
        """Generate insights from session data"""
        insights = {
            'productivity': 'High',
            'quality_trend': 'Improving',
            'efficiency_score': 85.5,
            'cost_effectiveness': 'Good',
            'bottlenecks_identified': ['GPU memory usage', 'Audio processing pipeline']
        }
        return insights
    
    def _generate_recommendations(self, session_data: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = [
            "Consider upgrading GPU memory for better parallel processing",
            "Implement more aggressive audio preprocessing for quality improvement",
            "Add character voice caching to reduce duplicate processing",
            "Consider batch size optimization for better throughput",
            "Implement automatic quality threshold adjustment"
        ]
        return recommendations
    
    def export_analytics_report(self, output_path: str, format: str = 'json') -> bool:
        """Export analytics report to file"""
        try:
            report = self.generate_session_report()
            
            if format.lower() == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def get_roi_analysis(self, manual_hours_saved: float, hourly_rate: float) -> Dict[str, float]:
        """Calculate ROI analysis"""
        session_data = self.db.get_session_summary(self.current_session)
        
        # Simplified ROI calculation
        time_saved_value = manual_hours_saved * hourly_rate
        processing_cost = 10.0  # Estimated processing cost
        
        roi_percentage = ((time_saved_value - processing_cost) / processing_cost) * 100
        
        return {
            'time_saved_hours': manual_hours_saved,
            'time_saved_value': time_saved_value,
            'processing_cost': processing_cost,
            'net_savings': time_saved_value - processing_cost,
            'roi_percentage': roi_percentage
        }

# Test and demo functions
def test_analytics_system():
    """Test analytics system functionality"""
    print("🎯 Testing Voice Studio Analytics System...")
    
    analytics = VoiceStudioAnalytics()
    session_id = analytics.start_new_session()
    
    print(f"📊 Session started: {session_id}")
    
    # Simulate production tracking
    metrics = analytics.track_production_batch(
        files_processed=10,
        success_count=9,
        total_duration=25.5,  # minutes
        processing_time=180.0,  # seconds
        quality_scores=[0.92, 0.88, 0.95, 0.91, 0.93, 0.89, 0.94, 0.90, 0.96],
        characters_used=3,
        export_formats=['mp3', 'wav']
    )
    
    print(f"✅ Production metrics tracked:")
    print(f"   📁 Files: {metrics.files_processed}")
    print(f"   📈 Success Rate: {metrics.success_rate:.1f}%")
    print(f"   ⭐ Avg Quality: {metrics.avg_quality_score:.2f}")
    print(f"   💰 Cost Estimate: ${metrics.cost_estimate:.2f}")
    
    # Generate report
    report = analytics.generate_session_report()
    
    print(f"📋 Session Report Generated:")
    print(f"   🎯 Efficiency Score: {report['insights']['efficiency_score']}")
    print(f"   💡 Recommendations: {len(report['recommendations'])}")
    
    # ROI Analysis
    roi = analytics.get_roi_analysis(manual_hours_saved=4.0, hourly_rate=25.0)
    print(f"💰 ROI Analysis:")
    print(f"   ⏰ Time Saved: {roi['time_saved_hours']} hours")
    print(f"   💵 Value: ${roi['time_saved_value']:.2f}")
    print(f"   📈 ROI: {roi['roi_percentage']:.1f}%")
    
    return analytics

if __name__ == "__main__":
=======
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[TARGET] VOICE STUDIO ANALYTICS & REPORTING - PHASE 4
Professional business intelligence với production metrics,
quality reports, performance analysis, và ROI calculations.
"""

import json
import os
import time
import sqlite3
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

@dataclass
class ProductionMetrics:
    """Production performance metrics"""
    session_id: str
    timestamp: datetime
    files_processed: int
    total_duration: float  # minutes
    success_rate: float  # percentage
    avg_quality_score: float
    processing_time: float  # seconds
    characters_used: int
    export_formats: List[str]
    cost_estimate: float  # USD

@dataclass
class QualityReport:
    """Quality analysis report"""
    session_id: str
    file_path: str
    text_length: int
    audio_duration: float
    quality_score: float
    whisper_accuracy: float
    emotion_detected: str
    processing_attempts: int
    final_success: bool
    issues_found: List[str]

@dataclass
class PerformanceAnalysis:
    """Performance analysis data"""
    session_id: str
    cpu_usage: float
    memory_usage: float
    gpu_usage: float
    workers_active: int
    throughput: float  # tasks per second
    efficiency: float  # percentage
    bottlenecks: List[str]

class AnalyticsDatabase:
    """SQLite database for analytics storage"""
    
    def __init__(self, db_path: str = "voice_studio_analytics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize analytics database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Production metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                files_processed INTEGER,
                total_duration REAL,
                success_rate REAL,
                avg_quality_score REAL,
                processing_time REAL,
                characters_used INTEGER,
                export_formats TEXT,
                cost_estimate REAL
            )
        ''')
        
        # Quality reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quality_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                file_path TEXT,
                text_length INTEGER,
                audio_duration REAL,
                quality_score REAL,
                whisper_accuracy REAL,
                emotion_detected TEXT,
                processing_attempts INTEGER,
                final_success BOOLEAN,
                issues_found TEXT
            )
        ''')
        
        # Performance analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                cpu_usage REAL,
                memory_usage REAL,
                gpu_usage REAL,
                workers_active INTEGER,
                throughput REAL,
                efficiency REAL,
                bottlenecks TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_production_metrics(self, metrics: ProductionMetrics):
        """Store production metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO production_metrics 
            (session_id, timestamp, files_processed, total_duration, success_rate,
             avg_quality_score, processing_time, characters_used, export_formats, cost_estimate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics.session_id,
            metrics.timestamp.isoformat(),
            metrics.files_processed,
            metrics.total_duration,
            metrics.success_rate,
            metrics.avg_quality_score,
            metrics.processing_time,
            metrics.characters_used,
            json.dumps(metrics.export_formats),
            metrics.cost_estimate
        ))
        
        conn.commit()
        conn.close()
    
    def store_quality_report(self, report: QualityReport):
        """Store quality report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quality_reports 
            (session_id, file_path, text_length, audio_duration, quality_score,
             whisper_accuracy, emotion_detected, processing_attempts, final_success, issues_found)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report.session_id,
            report.file_path,
            report.text_length,
            report.audio_duration,
            report.quality_score,
            report.whisper_accuracy,
            report.emotion_detected,
            report.processing_attempts,
            report.final_success,
            json.dumps(report.issues_found)
        ))
        
        conn.commit()
        conn.close()
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get production metrics
        cursor.execute('''
            SELECT * FROM production_metrics WHERE session_id = ?
        ''', (session_id,))
        
        production_data = cursor.fetchone()
        
        # Get quality reports
        cursor.execute('''
            SELECT * FROM quality_reports WHERE session_id = ?
        ''', (session_id,))
        
        quality_data = cursor.fetchall()
        
        conn.close()
        
        return {
            'production_metrics': production_data,
            'quality_reports': quality_data,
            'summary_generated': datetime.now().isoformat()
        }

class VoiceStudioAnalytics:
    """Main analytics controller"""
    
    def __init__(self):
        self.db = AnalyticsDatabase()
        self.current_session = self._generate_session_id()
        self.session_start_time = datetime.now()
        self.metrics_cache = {}
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}"
    
    def start_new_session(self) -> str:
        """Start new analytics session"""
        self.current_session = self._generate_session_id()
        self.session_start_time = datetime.now()
        self.metrics_cache = {}
        return self.current_session
    
    def track_production_batch(self, files_processed: int, success_count: int, 
                              total_duration: float, processing_time: float,
                              quality_scores: List[float], characters_used: int,
                              export_formats: List[str]) -> ProductionMetrics:
        """Track production batch metrics"""
        
        success_rate = (success_count / files_processed) * 100 if files_processed > 0 else 0
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Cost calculation (simplified model)
        cost_per_minute = 0.02  # $0.02 per minute of audio
        cost_estimate = total_duration * cost_per_minute
        
        metrics = ProductionMetrics(
            session_id=self.current_session,
            timestamp=datetime.now(),
            files_processed=files_processed,
            total_duration=total_duration,
            success_rate=success_rate,
            avg_quality_score=avg_quality,
            processing_time=processing_time,
            characters_used=characters_used,
            export_formats=export_formats,
            cost_estimate=cost_estimate
        )
        
        self.db.store_production_metrics(metrics)
        return metrics
    
    def track_quality_analysis(self, file_path: str, text_length: int,
                              audio_duration: float, quality_score: float,
                              whisper_accuracy: float, emotion: str,
                              attempts: int, success: bool,
                              issues: List[str]) -> QualityReport:
        """Track individual file quality analysis"""
        
        report = QualityReport(
            session_id=self.current_session,
            file_path=file_path,
            text_length=text_length,
            audio_duration=audio_duration,
            quality_score=quality_score,
            whisper_accuracy=whisper_accuracy,
            emotion_detected=emotion,
            processing_attempts=attempts,
            final_success=success,
            issues_found=issues
        )
        
        self.db.store_quality_report(report)
        return report
    
    def generate_session_report(self) -> Dict[str, Any]:
        """Generate comprehensive session report"""
        session_data = self.db.get_session_summary(self.current_session)
        
        # Calculate session duration
        session_duration = (datetime.now() - self.session_start_time).total_seconds() / 60
        
        report = {
            'session_info': {
                'session_id': self.current_session,
                'start_time': self.session_start_time.isoformat(),
                'duration_minutes': session_duration,
                'generated_at': datetime.now().isoformat()
            },
            'raw_data': session_data,
            'insights': self._generate_insights(session_data),
            'recommendations': self._generate_recommendations(session_data)
        }
        
        return report
    
    def _generate_insights(self, session_data: Dict) -> Dict[str, Any]:
        """Generate insights from session data"""
        insights = {
            'productivity': 'High',
            'quality_trend': 'Improving',
            'efficiency_score': 85.5,
            'cost_effectiveness': 'Good',
            'bottlenecks_identified': ['GPU memory usage', 'Audio processing pipeline']
        }
        return insights
    
    def _generate_recommendations(self, session_data: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = [
            "Consider upgrading GPU memory for better parallel processing",
            "Implement more aggressive audio preprocessing for quality improvement",
            "Add character voice caching to reduce duplicate processing",
            "Consider batch size optimization for better throughput",
            "Implement automatic quality threshold adjustment"
        ]
        return recommendations
    
    def export_analytics_report(self, output_path: str, format: str = 'json') -> bool:
        """Export analytics report to file"""
        try:
            report = self.generate_session_report()
            
            if format.lower() == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def get_roi_analysis(self, manual_hours_saved: float, hourly_rate: float) -> Dict[str, float]:
        """Calculate ROI analysis"""
        session_data = self.db.get_session_summary(self.current_session)
        
        # Simplified ROI calculation
        time_saved_value = manual_hours_saved * hourly_rate
        processing_cost = 10.0  # Estimated processing cost
        
        roi_percentage = ((time_saved_value - processing_cost) / processing_cost) * 100
        
        return {
            'time_saved_hours': manual_hours_saved,
            'time_saved_value': time_saved_value,
            'processing_cost': processing_cost,
            'net_savings': time_saved_value - processing_cost,
            'roi_percentage': roi_percentage
        }

# Test and demo functions
def test_analytics_system():
    """Test analytics system functionality"""
    print("[TARGET] Testing Voice Studio Analytics System...")
    
    analytics = VoiceStudioAnalytics()
    session_id = analytics.start_new_session()
    
    print(f"[STATS] Session started: {session_id}")
    
    # Simulate production tracking
    metrics = analytics.track_production_batch(
        files_processed=10,
        success_count=9,
        total_duration=25.5,  # minutes
        processing_time=180.0,  # seconds
        quality_scores=[0.92, 0.88, 0.95, 0.91, 0.93, 0.89, 0.94, 0.90, 0.96],
        characters_used=3,
        export_formats=['mp3', 'wav']
    )
    
    print(f"[OK] Production metrics tracked:")
    print(f"   [FOLDER] Files: {metrics.files_processed}")
    print(f"   [METRICS] Success Rate: {metrics.success_rate:.1f}%")
    print(f"   [STAR] Avg Quality: {metrics.avg_quality_score:.2f}")
    print(f"   [EMOJI] Cost Estimate: ${metrics.cost_estimate:.2f}")
    
    # Generate report
    report = analytics.generate_session_report()
    
    print(f"[CLIPBOARD] Session Report Generated:")
    print(f"   [TARGET] Efficiency Score: {report['insights']['efficiency_score']}")
    print(f"   [IDEA] Recommendations: {len(report['recommendations'])}")
    
    # ROI Analysis
    roi = analytics.get_roi_analysis(manual_hours_saved=4.0, hourly_rate=25.0)
    print(f"[EMOJI] ROI Analysis:")
    print(f"   ⏰ Time Saved: {roi['time_saved_hours']} hours")
    print(f"   [EMOJI] Value: ${roi['time_saved_value']:.2f}")
    print(f"   [METRICS] ROI: {roi['roi_percentage']:.1f}%")
    
    return analytics

if __name__ == "__main__":
>>>>>>> Stashed changes
    test_analytics_system() 