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

// Create job data
const jobData = {
  phoneNumber: '123-456-7890',
  message: 'Your code is 1234'
};

// Create a job
const job = queue.create('push_notification_code', jobData)
  .save((err) => {
    if (err) {
      console.error('Notification job creation failed:', err);
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });

// Handle job events
job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', (err) => {
  console.log(`Notification job failed: ${err.message}`);
});
