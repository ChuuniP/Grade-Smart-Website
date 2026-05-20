const fs = require('fs');

async function run() {
  try {
    const fileBuffer = fs.readFileSync('backend/uploads/MDD.jpg');
    const blob = new Blob([fileBuffer]);
    const file = new File([blob], 'MDD.jpg', { type: 'image/jpeg' });
    const formData = new FormData();
    formData.append('image', file);
    formData.append('answers', JSON.stringify(["B","C","C","C","D","D","C","B","D","A","A","A","B","C","C","C","D","B","A","C","B","C","C","C","D","D","C","B","D","A","A","A","B","C","C","C","D","B","A","C"]));

    console.log('Sending OMR request to backend...');
    const response = await fetch('http://localhost:3000/api/omr/process', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    console.log('Response Status:', response.status);
    console.log('Response Data:', JSON.stringify(data, null, 2));
  } catch (err) {
    console.error('Error during test:', err);
  }
}

run();
