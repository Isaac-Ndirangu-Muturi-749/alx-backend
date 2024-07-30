import kue from 'kue';
import redis from 'redis';

const client = redis.createClient();

// Create a Kue queue using the Redis client
const queue = kue.createQueue({
  redis: {
    host: '127.0.0.1',
    port: 6379
  }
});

// Define the function to send notification
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Process the jobs in the 'push_notification_code' queue
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message);
  done(); // Mark the job as complete
});

// Handle any job errors
queue.on('error', (err) => {
  console.error('Queue error:', err);
});
