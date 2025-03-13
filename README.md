# Algorithm Visualization

This directory contains a Java-based visualization tool for comparing **Merge Sort** and **Quick Sort** algorithms. The purpose of this project is to provide a visual representation of how these sorting algorithms work, making it easier to understand their behavior and differences.

## Features

- **Side-by-Side Visualization**: Compare Merge Sort and Quick Sort in real-time.
- **Dynamic Array Resizing**: The array visualization adjusts to fit the screen, even for larger arrays.
- **Color Coding**:
  - **Red**: Pivot element in Quick Sort.
  - **Yellow**: Active element being processed.
  - **Green**: Sorted portion of the array.
- **Interactive Controls**:
  - **Start Sorting**: Begins the sorting process for both algorithms.
  - **Reset**: Generates a new random array and resets the visualization.
  - **Pause/Resume**: Pauses or resumes the sorting process.

## How to Use

1. **Run the Program**:
   - Compile and run the `SortingHeapAndMergeUi` class.
   - A window will open with two panels: one for Quick Sort and one for Merge Sort.

2. **Start Sorting**:
   - Click the **Start Sorting** button to begin the sorting process.

3. **Pause/Resume**:
   - Use the **Pause/Resume** button to pause or resume the sorting process.

4. **Reset**:
   - Click the **Reset** button to generate a new random array and reset the visualization.

## Important Notes

- **Practice Project**: This project is intended for educational purposes and practice. It is not written to be taken too seriously or used in production environments.
- **Limited Libraries**: Not all Java libraries or best practices were used in this project. The focus was on simplicity and understanding the algorithms rather than optimizing the code.
- **Visualization Delay**: A delay is added between steps to make the sorting process easier to follow. This is not representative of the actual speed of the algorithms.

## Code Structure

- **`SortingHeapAndMergeUi`**: The main class that sets up the UI and handles the sorting logic.
- **`mergeSort` and `quickSort`**: Methods that implement the respective sorting algorithms.
- **`drawArray`**: Method responsible for visualizing the array in the UI.

## Dependencies

- **Java Swing**: Used for the graphical user interface.
- **Java AWT**: Used for drawing the array visualization.

## How to Contribute

If you'd like to improve this project, feel free to fork the repository and submit a pull request. Some ideas for improvements include:

- Adding more sorting algorithms (e.g., Bubble Sort, Insertion Sort).
- Improving the UI with additional controls or features.
- Optimizing the code for better performance.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

Enjoy visualizing and learning about sorting algorithms! 😊
