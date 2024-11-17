// [
// 	[
// 		1,
// 		"nut m42",
// 		"item1 description",
// 		"screw",
// 		10,
// 		1,
// 		2,
// 		"none"
// 	],
// 	[
// 		2,
// 		"nut m4456232",
// 		"item1 description",
// 		"screw",
// 		10,
// 		1,
// 		2,
// 		"none"
// 	],



document.addEventListener('DOMContentLoaded', function() {
    fetch('http://192.168.1.103:5000/api/list') 
        .then(response => response.json())
        .then(data => {
            // Sort the data by node > position > name
            data.sort((a, b) => {
                if (a[5] === b[5]) {
                    if (a[6] === b[6]) {
                        return a[1].localeCompare(b[1]);
                    }
                    return a[6] - b[6];
                }
                return a[5] - b[5];
            });

            const tableBody = document.getElementById('itemTable').getElementsByTagName('tbody')[0];
            data.forEach(item => {
                const row = tableBody.insertRow();
                // Start inserting cells from the second element (index 1)
                for (let i = 1; i < item.length; i++) {
                    if (i === 4) {
                        const cell = row.insertCell(i - 1);
                        const input = document.createElement('input');
                        input.type = 'number';
                        input.value = item[i];
                        input.classList.add('quantityInputNum');
                        cell.appendChild(input);
                    } else {
                        if (i === 7) {
                            continue;
                        }
                    {
                        if (i === 1) {
                            if (item[7] !== "none") {
                                const cell = row.insertCell(i - 1);
                                const link = document.createElement('a');
                                link.href = item[7];
                                link.textContent = item[i];
                                cell.appendChild(link);
                            } else {
                                row.insertCell(i - 1).textContent = item[i];
                            }
                        } else {
                            row.insertCell(i - 1).textContent = item[i];
                        }
                    }
                  }
                }

        const quantityCell = row.insertCell(item.length - 2);
        const quantityInput = row.querySelector('.quantityInputNum');
        quantityInput.addEventListener('change', () => {
            // Add functionality to handle quantity change here
            console.log('Quantity changed for item:', item[0], 'New quantity:', quantityInput.value);
            quantity_item(item[0], quantityInput.value);
        });

        // Add "Delete" button
        const deleteCell = row.insertCell(item.length - 2);
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => {
            // Add delete functionality here
            // console.log('Delete button clicked for item:', item[0]);
            deleteItem(item[0]);
            window.location.reload();

        });
        deleteCell.appendChild(deleteButton);

        // Add "Locate" button
        const locateCell = row.insertCell(item.length - 1);
        const locateButton = document.createElement('button');
        locateButton.textContent = 'Locate';
        locateButton.addEventListener('click', () => {
            // Add locate functionality here
            // console.log('Locate button clicked for item:', item[0]);
            locateItem(item[0]);
        });
        locateCell.appendChild(locateButton);
        });
        })
        .catch(error => console.error('Error fetching data:', error));
});

function quantity_item(id, quantity){
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'User-Agent': 'insomnia/10.1.1'},
        body: '{"id":' + id + ',"quantity":' + quantity + '}'
      };
      
      fetch('http://127.0.0.1:5000/api/quantity', options)
        .then(response => response.json())
        .then(response => console.log(response))
        .catch(err => console.error(err));

}

function locateItem(id){
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: '{"id":' + id + '}'
      };
      
      fetch('http://192.168.1.103:5000/api/locate', options)
        .then(response => response.json())
        .then(response => console.log(response))
        .catch(err => console.error(err));

}

function deleteItem(id){
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: '{"id":' + id + '}'
      };
      
      fetch('http://127.0.0.1:5000/api/delete', options)
        .then(response => response.json())
        .then(response => console.log(response))
        .catch(err => console.error(err));
}