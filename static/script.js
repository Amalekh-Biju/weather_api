 document.addEventListener('DOMContentLoaded', () => {
      const locationInput = document.getElementById('locationInput');
      const getWeatherButton = document.getElementById('getWeatherButton');
      const weatherResultDiv = document.getElementById('weatherResult');
      const errorMessagesDiv = document.getElementById('errorMessages');

      const getRandomWeatherButton = document.getElementById('getRandomWeatherButton');
      const randomWeatherResultDiv = document.getElementById('randomWeatherResult');
      const getGlobalAverageButton = document.getElementById('getGlobalAverageButton');
      const globalAverageResultDiv = document.getElementById('globalAverageResult');

      const displayWeatherData = (data, element) => {
          element.innerHTML = `
              <p><strong>Location:</strong> ${data.location || 'N/A'}</p>
              <p><strong>Temperature:</strong> ${data.temperature || 'N/A'}</p>
              <p><strong>Humidity:</strong> ${data.humidity || 'N/A'}</p>
              ${data.condition ? `<p><strong>Condition:</strong> ${data.condition}</p>` : ''}
              ${data.description ? `<p><strong>Description:</strong> ${data.description}</p>` : ''}
          `;
          errorMessagesDiv.textContent = ''; // Clear previous errors
      };

      const displayError = (message) => {
          weatherResultDiv.innerHTML = ''; // Clear previous results
          errorMessagesDiv.textContent = message;
      };
      
      const clearOtherResults = () => {
          randomWeatherResultDiv.innerHTML = '';
          globalAverageResultDiv.innerHTML = '';
      };

      getWeatherButton.addEventListener('click', async () => {
          const location = locationInput.value.trim();
          if (!location) {
              displayError('Please enter a city name.');
              return;
          }
          clearOtherResults();

          try {
              const response = await fetch(`/weather/${encodeURIComponent(location)}`);
              if (!response.ok) {
                  const errorData = await response.json();
                  throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
              }
              const data = await response.json();
              displayWeatherData(data, weatherResultDiv);
          } catch (error) {
              console.error('Error fetching weather:', error);
              displayError(`Eda Mone 5 times athilum kooduthal 5 mins il pattula ketto 
                Failed to fetch weather: ${error.message}`);
          }
      });

      locationInput.addEventListener('keypress', (event) => {
          if (event.key === 'Enter') {
              getWeatherButton.click();
          }
      });

      getRandomWeatherButton.addEventListener('click', async () => {
          weatherResultDiv.innerHTML = ''; 
          globalAverageResultDiv.innerHTML = '';
          try {
              const response = await fetch('/weather/random/location');
              if (!response.ok) {
                  const errorData = await response.json();
                  throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
              }
              const data = await response.json();
              displayWeatherData(data, randomWeatherResultDiv);
          } catch (error) {
              console.error('Error fetching random weather:', error);
              randomWeatherResultDiv.innerHTML = `<p style="color: red;">Eda Mone 5 times athilum kooduthal 5 mins il pattula ketto
              Failed to fetch random weather: ${error.message}</p>`;
          }
      });

      getGlobalAverageButton.addEventListener('click', async () => {
          weatherResultDiv.innerHTML = ''; // Clear main result
          randomWeatherResultDiv.innerHTML = '';
          try {
              const response = await fetch('/weather/global/average');
              if (!response.ok) {
                  const errorData = await response.json();
                  throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
              }
              const data = await response.json();
              displayWeatherData(data, globalAverageResultDiv);
          } catch (error) {
              console.error('Error fetching global average weather:', error);
              globalAverageResultDiv.innerHTML = `<p style="color: red;">Eda Mone 5 times athilum kooduthal 5 mins il pattula ketto
              Failed to fetch global average: ${error.message} </p>`;
          }
      });
  });