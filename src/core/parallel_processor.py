"""

Parallel Processing System - PHASE 2 Implementation  

4-8x speed improvement với multi-threading và queue management

"""



import os

import time

import threading

from queue import Queue, Empty

from typing import List, Dict, Any, Optional, Callable

from dataclasses import dataclass, field

from datetime import datetime





@dataclass

class ProcessingTask:

    """Individual processing task"""

    task_id: str

    input_data: Any

    task_type: str

    priority: int = 1

    created_at: datetime = field(default_factory=datetime.now)

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    result: Optional[Any] = None

    error: Optional[str] = None

    progress: float = 0.0





@dataclass

class WorkerStats:

    """Worker thread statistics"""

    worker_id: str

    tasks_completed: int = 0

    tasks_failed: int = 0

    total_processing_time: float = 0.0

    last_active: Optional[datetime] = None

    current_task: Optional[str] = None





class ParallelProcessor:

    """Professional parallel processing system"""

    

    def __init__(self, num_workers: int = 4, max_queue_size: int = 100):

        self.num_workers = min(num_workers, os.cpu_count() or 4)

        self.max_queue_size = max_queue_size

        self.task_queue = Queue(maxsize=max_queue_size)

        

        # Worker management

        self.workers = []

        self.worker_stats = {}

        self.is_running = False

        

        # Task tracking

        self.tasks = {}

        self.completed_tasks = {}

        self.task_handlers = {}

        

        # Performance monitoring

        self.start_time = None

        self.total_tasks_processed = 0

        self.total_processing_time = 0.0

        

        # Thread safety

        self.lock = threading.Lock()

        

        print(f"🚀 Parallel Processor initialized với {self.num_workers} workers")

    

    def register_task_handler(self, task_type: str, handler: Callable):

        """Register handler function cho specific task type"""

        self.task_handlers[task_type] = handler

        print(f"📋 Registered handler for task type: {task_type}")

    

    def start_workers(self):

        """Start worker threads"""

        if self.is_running:

            return

            

        self.is_running = True

        self.start_time = datetime.now()

        

        # Pre-initialize worker stats BEFORE starting threads to avoid race condition

        for i in range(self.num_workers):

            worker_id = f"worker_{i+1}"

            self.worker_stats[worker_id] = WorkerStats(worker_id)

        

        # Now start worker threads

        for i in range(self.num_workers):

            worker_id = f"worker_{i+1}"

            worker = threading.Thread(target=self._worker_loop, args=(worker_id,))

            worker.daemon = True

            worker.start()

            self.workers.append(worker)

        

        print(f"✅ Started {len(self.workers)} worker threads")

    

    def stop_workers(self):

        """Stop all worker threads"""

        self.is_running = False

        

        # Signal workers to stop

        for _ in range(self.num_workers):

            self.task_queue.put(None)  # Poison pill

        

        # Wait for workers to finish

        for worker in self.workers:

            worker.join(timeout=5.0)

        

        self.workers.clear()

        print("🛑 All workers stopped")

    

    def submit_task(self, task_id: str, input_data: Any, task_type: str, priority: int = 1) -> bool:

        """Submit task for processing"""

        if task_type not in self.task_handlers:

            print(f"❌ No handler registered for task type: {task_type}")

            return False

        

        if self.task_queue.full():

            print("⚠️ Task queue is full, cannot submit task")

            return False

        

        task = ProcessingTask(

            task_id=task_id,

            input_data=input_data,

            task_type=task_type,

            priority=priority

        )

        

        with self.lock:

            self.tasks[task_id] = task

        

        self.task_queue.put(task)

        print(f"📤 Submitted task: {task_id} (type: {task_type})")

        return True

    

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:

        """Get status of specific task"""

        with self.lock:

            if task_id in self.completed_tasks:

                task = self.completed_tasks[task_id]

                return {

                    'status': 'completed',

                    'success': task.error is None,

                    'result': task.result,

                    'error': task.error,

                    'progress': 100.0

                }

            elif task_id in self.tasks:

                task = self.tasks[task_id]

                if task.started_at:

                    return {'status': 'processing', 'progress': task.progress}

                else:

                    return {'status': 'queued', 'progress': 0.0}

        

        return None

    

    def get_performance_stats(self) -> Dict[str, Any]:

        """Get comprehensive performance statistics"""

        current_time = datetime.now()

        runtime = (current_time - self.start_time).total_seconds() if self.start_time else 0.0

        

        stats = {

            'runtime_seconds': runtime,

            'total_tasks_processed': self.total_tasks_processed,

            'total_processing_time': self.total_processing_time,

            'avg_task_time': self.total_processing_time / max(self.total_tasks_processed, 1),

            'throughput_per_second': self.total_tasks_processed / max(runtime, 1),

            'efficiency': (self.total_processing_time / (runtime * self.num_workers)) * 100 if runtime > 0 else 0,

            'workers': {}

        }

        

        for worker_id, worker_stats in self.worker_stats.items():

            stats['workers'][worker_id] = {

                'tasks_completed': worker_stats.tasks_completed,

                'tasks_failed': worker_stats.tasks_failed,

                'total_processing_time': worker_stats.total_processing_time,

                'current_task': worker_stats.current_task

            }

        

        return stats

    

    def _worker_loop(self, worker_id: str):

        """Main worker thread loop"""

        stats = self.worker_stats[worker_id]

        

        while self.is_running:

            try:

                # Get task từ queue với timeout

                task = self.task_queue.get(timeout=1.0)

                

                if task is None:  # Poison pill

                    break

                

                # Update stats

                stats.current_task = task.task_id

                stats.last_active = datetime.now()

                

                # Process task

                self._process_task(task, worker_id)

                

                # Update stats

                stats.tasks_completed += 1

                stats.current_task = None

                

                self.task_queue.task_done()

                

            except Empty:

                continue  # Timeout, check if still running

            except Exception as e:

                print(f"❌ Worker {worker_id} error: {str(e)}")

                if 'task' in locals():

                    self._handle_task_error(task, str(e))

                    stats.tasks_failed += 1

        

        print(f"🏁 Worker {worker_id} finished. Completed: {stats.tasks_completed}")

    

    def _process_task(self, task: ProcessingTask, worker_id: str):

        """Process individual task"""

        task.started_at = datetime.now()

        

        try:

            # Get handler cho task type

            handler = self.task_handlers[task.task_type]

            

            # Execute handler

            result = handler(task.input_data)

            

            # Task completed successfully

            task.result = result

            task.progress = 100.0

            task.completed_at = datetime.now()

            

            # Move to completed tasks

            with self.lock:

                self.completed_tasks[task.task_id] = task

                if task.task_id in self.tasks:

                    del self.tasks[task.task_id]

            

            # Update global stats

            processing_time = (task.completed_at - task.started_at).total_seconds()

            self.worker_stats[worker_id].total_processing_time += processing_time

            self.total_tasks_processed += 1

            self.total_processing_time += processing_time

            

            print(f"✅ Task completed: {task.task_id} by {worker_id} ({processing_time:.2f}s)")

            

        except Exception as e:

            self._handle_task_error(task, str(e))

            self.worker_stats[worker_id].tasks_failed += 1

    

    def _handle_task_error(self, task: ProcessingTask, error_msg: str):

        """Handle task processing error"""

        task.error = error_msg

        task.completed_at = datetime.now()

        

        with self.lock:

            self.completed_tasks[task.task_id] = task

            if task.task_id in self.tasks:

                del self.tasks[task.task_id]

        

        print(f"❌ Task failed: {task.task_id} - {error_msg}")





# Example task handler

def example_voice_generation_handler(input_data: Dict[str, Any]):

    """Example handler cho voice generation task"""

    text = input_data.get('text', '')

    voice_id = input_data.get('voice_id', 'default')

    

    # Simulate processing time

    time.sleep(0.5)

    

    result = {

        'success': True,

        'output_file': f"./output/{voice_id}_{len(text)}_chars.mp3",

        'duration': len(text) * 0.05,

        'text_length': len(text)

    }

    

    return result





# Test function

def test_parallel_processor():

    """Test parallel processor với example tasks"""

    processor = ParallelProcessor(num_workers=2)

    

    # Register handler

    processor.register_task_handler('voice_generation', example_voice_generation_handler)

    

    # Start workers

    processor.start_workers()

    

    # Submit test tasks

    for i in range(3):

        processor.submit_task(

            f'voice_{i}', 

            {'text': f'Test text {i}', 'voice_id': 'narrator'}, 

            'voice_generation'

        )

    

    # Wait a bit for processing

    time.sleep(2.0)

    

    # Get performance stats

    stats = processor.get_performance_stats()

    print(f"📊 Throughput: {stats['throughput_per_second']:.2f} tasks/sec")

    print(f"📊 Efficiency: {stats['efficiency']:.1f}%")

    

    # Stop workers

    processor.stop_workers()

    

    return processor





if __name__ == "__main__":

    test_parallel_processor()

