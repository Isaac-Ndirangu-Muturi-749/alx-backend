import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let queue;

  before(() => {
    // Create a Kue queue and enter test mode
    queue = kue.createQueue();
    queue.testMode = true;
  });

  afterEach(() => {
    // Clear the queue after each test
    queue.testMode.clear();
  });

  after(() => {
    // Exit test mode
    queue.testMode = false;
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('should create jobs and log job creation', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'Test message 1' },
      { phoneNumber: '4153518781', message: 'Test message 2' }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Check that the jobs are in the queue
    const queueJobs = queue.testMode.jobs();
    expect(queueJobs).to.have.lengthOf(2);

    // Validate job details
    expect(queueJobs[0].type).to.equal('push_notification_code_3');
    expect(queueJobs[1].type).to.equal('push_notification_code_3');
  });
});
