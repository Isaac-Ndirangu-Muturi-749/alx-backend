import kue from 'kue';

// Define the function createPushNotificationsJobs
const createPushNotificationsJobs = (jobs, queue) => {
  // Check if jobs is an array
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // Iterate through each job and add it to the queue
  jobs.forEach(jobData => {
    // Create a job in the queue
    const job = queue.create('push_notification_code_3', jobData)
      .save(err => {
        if (err) {
          console.error('Error creating job:', err);
        } else {
          console.log(`Notification job created: ${job.id}`);
        }
      });

    // Listen for job events
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    }).on('failed', (errorMessage) => {
      console.log(`Notification job ${job.id} failed: ${errorMessage}`);
    }).on('progress', (progress, data) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  });
};

export default createPushNotificationsJobs;
