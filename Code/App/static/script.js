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



// document.addEventListener('DOMContentLoaded', function() {
//     fetch('http://192.168.1.103:5000/api/list') 
//         .then(response => response.json())
//         .then(data => {
//             // Sort the data by node > position > name
//             data.sort((a, b) => {
//                 if (a[5] === b[5]) {
//                     if (a[6] === b[6]) {
//                         return a[1].localeCompare(b[1]);
//                     }
//                     return a[6] - b[6];
//                 }
//                 return a[5] - b[5];
//             });

//             const tableBody = document.getElementById('itemTable').getElementsByTagName('tbody')[0];
//             data.forEach(item => {
//                 const row = tableBody.insertRow();
//                 // Start inserting cells from the second element (index 1)
//                 for (let i = 1; i < item.length; i++) {
//                     if (i === 4) {
//                         const cell = row.insertCell(i - 1);
//                         const input = document.createElement('input');
//                         input.type = 'number';
//                         input.value = item[i];
//                         input.classList.add('quantityInputNum');
//                         cell.appendChild(input);
//                     } else {
//                         if (i === 7) {
//                             continue;
//                         }
//                     {
//                         if (i === 1) {
//                             if (item[7] !== "none") {
//                                 const cell = row.insertCell(i - 1);
//                                 const link = document.createElement('a');
//                                 link.href = item[7];
//                                 link.textContent = item[i];
//                                 cell.appendChild(link);
//                             } else {
//                                 row.insertCell(i - 1).textContent = item[i];
//                             }
//                         } else {
//                             row.insertCell(i - 1).textContent = item[i];
//                         }
//                     }
//                   }
//                 }

//         const quantityCell = row.insertCell(item.length - 2);
//         const quantityInput = row.querySelector('.quantityInputNum');
//         quantityInput.addEventListener('change', () => {
//             // Add functionality to handle quantity change here
//             console.log('Quantity changed for item:', item[0], 'New quantity:', quantityInput.value);
//             quantity_item(item[0], quantityInput.value);
//         });

//         // Add "Delete" button
//         const deleteCell = row.insertCell(item.length - 2);
//         const deleteButton = document.createElement('button');
//         deleteButton.textContent = 'Delete';
//         deleteButton.addEventListener('click', () => {
//             // Add delete functionality here
//             // console.log('Delete button clicked for item:', item[0]);
//             deleteItem(item[0]);
//             window.location.reload();

//         });
//         deleteCell.appendChild(deleteButton);

//         // Add "Locate" button
//         const locateCell = row.insertCell(item.length - 1);
//         const locateButton = document.createElement('button');
//         locateButton.textContent = 'Locate';
//         locateButton.addEventListener('click', () => {
//             // Add locate functionality here
//             // console.log('Locate button clicked for item:', item[0]);
//             locateItem(item[0]);
//         });
//         locateCell.appendChild(locateButton);
//         });
//         })
//         .catch(error => console.error('Error fetching data:', error));

//         // const addItemDialogButton = document.getElementById('addItemDialog');
//         // addItemDialogButton.addEventListener('click', () => {
//         //     addItemDialog();
//         // });
        
//         // const addNodeDialogButton = document.getElementById('addNodeDialog');
//         // addNodeDialogButton.addEventListener('click', () => {
//         //     addNodeDialog();
//         // });
// });

var server = "192.168.1.105"; // Server IP address

document.addEventListener('DOMContentLoaded', (event) => {

    
    const categoryInput = document.getElementById('categoryInput');
    const nameInput = document.getElementById('nameInput');
    const tableBody = document.getElementById('itemTable').getElementsByTagName('tbody')[0];

    // Function to update the table based on the category input
    function updateTable() {
        // Clear the existing table rows
        tableBody.innerHTML = '';

        console.log(data)
        // Filter and display the items
        data.forEach(item => {
            // console.log(item.length)
            if (!categoryInput || item[3].toLowerCase().includes(categoryInput.value.toLowerCase())) {

                if (!nameInput || item[1].toLowerCase().includes(nameInput.value.toLowerCase())) {

                const row = tableBody.insertRow();
                for (let i = 1; i < item.length; i++) {
                    if (i === 4) {
                        const cell = row.insertCell(i - 1);
                        const input = document.createElement('input');
                        input.type = 'number';
                        input.value = item[i];
                        input.classList.add('quantityInputNum');
                        cell.appendChild(input);
                    } else if (i === 7) {
                        continue;
                    } else {
                        
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
                            if (i === 3) {
                                row.insertCell(i - 1).textContent = capitalizeFirstLetter(item[i]);
                            } else{
                                row.insertCell(i - 1).textContent = item[i];
                            }
                            
                        }
                    }
                
                }

                // const quantityCell = row.insertCell(item.length - 2);
                const quantityInput = row.querySelector('.quantityInputNum');
                quantityInput.addEventListener('change', () => {
                    // Add functionality to handle quantity change here
                    console.log('Quantity changed for item:', item[0], 'New quantity:', quantityInput.value);
                    quantity_item(item[0], quantityInput.value);
                });
        
                // Add "Delete" button
                const deleteCell = row.insertCell(6);
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
                const locateCell = row.insertCell(7);
                const locateButton = document.createElement('button');
                locateButton.textContent = 'Locate';
                locateButton.addEventListener('click', () => {
                    // Add locate functionality here
                    // console.log('Locate button clicked for item:', item[0]);
                    locateItem(item[0]);
                });
                locateCell.appendChild(locateButton);

                // Add "Edit" button
                const editCell = row.insertCell(8);
                const editButton = document.createElement('button');
                editButton.textContent = 'Edit';
                editButton.addEventListener('click', () => {
                    // Add edit functionality here
                    // console.log('Edit button clicked for item:', item[0]);
                    // editItem(item[0]);
                    editItem(item[0]);
                });
                editCell.appendChild(editButton);

            }
        }
        });
        
    }
    

    fetch('http://'+ server+ ':5000/api/list') 
    .then(response => response.json())
    .then(fetchedData => {
        // Sort the data by node > position > name
        fetchedData.sort((a, b) => {
            if (a[5] === b[5]) {
                if (a[6] === b[6]) {
                    return a[1].localeCompare(b[1]);
                }
                return a[6] - b[6];
            }
            return a[5] - b[5];
        });
        
        data = fetchedData;
        updateTable();
    });
        
    // Add event listener to the category input
    if (categoryInput) {
        categoryInput.addEventListener('input', updateTable);
    }
    
    if (nameInput) {
        nameInput.addEventListener('input', updateTable);
    }
    // // Initial table update
    // updateTable();
});

document.addEventListener('DOMContentLoaded', (event) => {
    const addItemDialog = document.getElementById('addItemDialog');
    const addItemDialogButton = document.getElementById('addItemDialogButton');
    const closeDialogButton = document.getElementById('closeDialog');
    const addItemForm = document.getElementById('addItemForm');

    if (addItemDialogButton && addItemDialog && closeDialogButton && addItemForm) {
        addItemDialogButton.addEventListener('click', () => {
            addItemDialog.showModal();
        });

        closeDialogButton.addEventListener('click', () => {
            addItemDialog.close();
        });

        addItemForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevent the default form submission

            const formData = new FormData(addItemForm);

            

            const expression = /[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/gi;
            const regex = new RegExp(expression);
            const t = formData.get('link');
            let link;
            if (t.match(regex)) {
              link = formData.get('link');
            } else {
              link = 'none';
            }

            const itemData = {
                name: formData.get('name'),
                description: formData.get('description'),
                category: capitalizeFirstLetter(formData.get('category')),
                quantity: parseInt(formData.get('quantity')),
                node: parseInt(formData.get('node')),
                position: parseInt(formData.get('slot')),
                url: link
            };

            console.log('Form Data:', itemData);

            // You can now send the itemData to your server or process it as needed
            const options = {
                method: 'POST',
                headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                body: JSON.stringify(itemData)
            };

            fetch('http://'+ server+ ':5000/api/additem', options)
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    addItemDialog.close(); // Close the dialog after successful submission
                    window.location.reload();
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        });
    } else {
        console.error('One or more elements are not found in the DOM.');
    }

});

document.addEventListener('DOMContentLoaded', (event) => {
    function editItem(id){
        const editItemDialog = document.getElementById('editItemDialog');
        const closeEditDialogButton = document.getElementById('closeEditDialog');
        const editItemForm = document.getElementById('editItemForm');

        
        if (editItemDialog && closeEditDialogButton && editItemForm) {
        editItemDialog.showModal();
    
        closeEditDialogButton.addEventListener('click', () => {
            editItemDialog.close();
        });
        // set placeholder text to current values
        fetch('http://'+ server+ ':5000/api/list?id=' + id)
        .then(response => response.json())
        .then(data => {

            editItemForm.elements['editName'].placeholder = data[0][1];
            editItemForm.elements['editDescription'].placeholder = data[0][2];
            editItemForm.elements['editCategory'].placeholder = data[0][3];
            editItemForm.elements['editQuantity'].placeholder = data[0][4];
            editItemForm.elements['editNode'].placeholder = data[0][5];
            editItemForm.elements['editSlot'].placeholder = data[0][6];
            editItemForm.elements['editLink'].placeholder = data[0][7];
        })
        .catch(error => console.error('Error fetching data:', error));

        editItemForm.addEventListener('submit', (event) => {
        // event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(editItemForm);

        // const expression = /[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/gi;
        // const regex = new RegExp(expression);
        // const t = formData.get('editLink');
        // let link;

        // if (t.match(regex)) {
        //     link = formData.get('editLink');
        // } else {
        //     link = 'none';
        // }
        // print(formData);

        const itemData = {
            id: id,
            name: formData.get('editName') !== '' ? formData.get('editName') : editItemForm.elements['editName'].placeholder,
            description: formData.get('editDescription') !== '' ? formData.get('editDescription') : editItemForm.elements['editDescription'].placeholder,
            category: formData.get('editCategory') !== '' ? capitalizeFirstLetter(formData.get('editCategory')) : capitalizeFirstLetter(editItemForm.elements['editCategory'].placeholder),
            quantity: formData.get('editQuantity') !== '' ? parseInt(formData.get('editQuantity')) : parseInt(editItemForm.elements['editQuantity'].placeholder),
            node: formData.get('editNode') !== '' ? parseInt(formData.get('editNode')) : parseInt(editItemForm.elements['editNode'].placeholder),
            position: formData.get('editSlot') !== '' ? parseInt(formData.get('editSlot')) : parseInt(editItemForm.elements['editSlot'].placeholder),
            url: formData.get('editLink') !== '' ? formData.get('editLink') : editItemForm.elements['editLink'].placeholder
        };
        // print(formData);
        // console.log(formData);
        // console.log(itemData);
        // console.log(formData.get('editName'))
        // console.log(JSON.stringify(itemData));
        // console.log(data);
        // print(itemData);
        // print(JSON.stringify(itemData));
        // console.log(itemData);
        const options = {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            body: JSON.stringify(itemData)
          };
          
          fetch('http://'+ server+ ':5000/api/edit', options)
            .then(response => response.json())
            .then(response => console.log(response))
            .catch(err => console.error(err));
            // print('Success:', data);
            editItemDialog.close(); // Close the dialog after successful submission
            window.location.reload();

        
    });
        } else {
            console.error('One or more elements are not found in the DOM.');
            console.log('editItemDialog:', editItemDialog);
            console.log('closeEditDialogButton:', closeEditDialogButton);
            console.log('editItemForm:', editItemForm);
        }
    }

    window.editItem = editItem;
});

function quantity_item(id, quantity){
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        body: '{"id":' + id + ',"quantity":' + quantity + '}'
      };
      
      fetch('http://'+ server+ ':5000/api/quantity', options)
        .then(response => response.json())
        .then(response => console.log(response))
        .catch(err => console.error(err));

}

function locateItem(id){
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        body: '{"id":' + id + '}'
      };
      
      fetch('http://'+ server+ ':5000/api/locate', options)
        .then(response => response.json())
        .then(response => console.log(response))
        .catch(err => console.error(err));

}


function deleteItem(id){
    const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        body: '{"id":' + id + '}'
      };
      
      fetch('http://'+ server+ ':5000/api/delete', options)
        .then(response => response.json())
        .then(response => console.log(response))
        .catch(err => console.error(err));
}

function capitalizeFirstLetter(string) {
    if (!string) return string;
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}