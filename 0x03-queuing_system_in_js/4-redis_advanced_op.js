import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Function to create hash
function createHash() {
  const hashKey = 'HolbertonSchools';
  const hashFields = {
    Portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2,
  };

  Object.entries(hashFields).forEach(([field, value]) => {
    client.hset(hashKey, field, value, redis.print);
  });
}

// Function to display hash
function displayHash() {
  client.hgetall('HolbertonSchools', (err, obj) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log(obj);
  });
}

// Create the hash and then display it
createHash();
displayHash();
