import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;
import javax.swing.*;

public class SortingHeapAndMergeUi extends JFrame {

    private JTextArea feedbackArea; 
    private JPanel quickSortPanel; 
    private JPanel mergeSortPanel; 
    private int[] quickSortArray; 
    private int[] mergeSortArray; 
    private int activeIndex = -1;
    private int pivotIndex = -1; 
    private int sortedIndex = -1; 
    private boolean isSorting = false; 
    private boolean isPaused = false; 
    private Thread sortingThread; 

    public SortingHeapAndMergeUi() {
        setTitle("Quick Sort vs Merge Sort Visualization");
        setSize(1200, 700);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());

        feedbackArea = new JTextArea();
        feedbackArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(feedbackArea);

        quickSortPanel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                drawArray(g, quickSortArray, "Quick Sort");
            }
        };
        quickSortPanel.setPreferredSize(new Dimension(600, 300));

        mergeSortPanel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                drawArray(g, mergeSortArray, "Merge Sort");
            }
        };
        mergeSortPanel.setPreferredSize(new Dimension(600, 300));

        JPanel visualizationPanel = new JPanel();
        visualizationPanel.setLayout(new GridLayout(1, 2)); 
        visualizationPanel.add(quickSortPanel);
        visualizationPanel.add(mergeSortPanel);

        JButton startButton = new JButton("Start Sorting");
        JButton resetButton = new JButton("Reset");
        JButton pauseButton = new JButton("Pause/Resume");

        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (!isSorting) {
                    isSorting = true;
                    feedbackArea.setText(""); 
                    sortingThread = new Thread(() -> {
                        quickSort(quickSortArray, 0, quickSortArray.length - 1);
                        mergeSort(mergeSortArray, 0, mergeSortArray.length - 1);
                        feedbackArea.append("Sorting complete!\n");
                        isSorting = false;
                    });
                    sortingThread.start();
                }
            }
        });

        resetButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (isSorting) {
                    sortingThread.interrupt(); 
                    isSorting = false;
                }
                initializeArrays(10); 
                feedbackArea.setText("Array reset.\n");
                quickSortPanel.repaint();
                mergeSortPanel.repaint();
            }
        });

        pauseButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                isPaused = !isPaused; 
                if (isPaused) {
                    feedbackArea.append("Sorting paused.\n");
                } else {
                    feedbackArea.append("Sorting resumed.\n");
                }
            }
        });

        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new FlowLayout());
        buttonPanel.add(startButton);
        buttonPanel.add(resetButton);
        buttonPanel.add(pauseButton);

        panel.add(visualizationPanel, BorderLayout.CENTER);
        panel.add(scrollPane, BorderLayout.EAST);
        panel.add(buttonPanel, BorderLayout.SOUTH);

        add(panel);

        initializeArrays(10);

        setVisible(true);
    }

    private void initializeArrays(int size) {
        quickSortArray = new int[size];
        mergeSortArray = new int[size];
        Random rand = new Random();
        for (int i = 0; i < size; i++) {
            int value = rand.nextInt(100) + 1;
            quickSortArray[i] = value;
            mergeSortArray[i] = value;
        }
        sortedIndex = -1; // Reset sorted index
        activeIndex = -1; // Reset active index
        pivotIndex = -1; // Reset pivot index
        quickSortPanel.repaint();
        mergeSortPanel.repaint();
    }

    private void drawArray(Graphics g, int[] array, String algorithm) {
        int arrayWidth = array.length > 0 ? getWidth() / 2 : 0; 
        int cellWidth = arrayWidth / array.length; 
        int cellHeight = 50; 
        int startX = 10; 
        int startY = 10; 

        for (int i = 0; i < array.length; i++) {
            if (i == pivotIndex && algorithm.equals("Quick Sort")) {
                g.setColor(Color.RED); 
            } else if (i == activeIndex) {
                g.setColor(Color.YELLOW); 
            } else if (i <= sortedIndex) {
                g.setColor(Color.GREEN); 
            } else {
                g.setColor(Color.LIGHT_GRAY); 
            }

            g.fillRect(startX + i * cellWidth, startY, cellWidth, cellHeight);
            g.setColor(Color.BLACK);
            g.drawRect(startX + i * cellWidth, startY, cellWidth, cellHeight);

            g.setColor(Color.BLACK);
            g.drawString(Integer.toString(array[i]), startX + i * cellWidth + 5, startY + 30);
        }

        g.setColor(Color.BLACK);
        g.drawString(algorithm, startX + 10, startY + cellHeight + 20);
    }

    private void mergeSort(int[] array, int left, int right) {
        if (left < right) {
            int mid = (left + right) / 2;
            mergeSort(array, left, mid);
            mergeSort(array, mid + 1, right);
            merge(array, left, mid, right);
        }
    }

    private void merge(int[] array, int left, int mid, int right) {
        int[] temp = new int[array.length];
        System.arraycopy(array, left, temp, left, right - left + 1);

        int i = left, j = mid + 1, k = left;
        while (i <= mid && j <= right) {
            if (isPaused) {
                while (isPaused) {
                    try {
                        Thread.sleep(100); 
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }
            }
            if (temp[i] <= temp[j]) {
                array[k++] = temp[i];
                activeIndex = k - 1; 
                updateFeedback("Merge Sort: Merging elements: " + temp[i] + " and " + temp[j]);
                i++; 
            } else {
                array[k++] = temp[j];
                activeIndex = k - 1; 
                updateFeedback("Merge Sort: Merging elements: " + temp[i] + " and " + temp[j]);
                j++; 
            }
            mergeSortPanel.repaint();
            sleep(500); 
        }
        while (i <= mid) {
            array[k++] = temp[i++];
        }
        while (j <= right) {
            array[k++] = temp[j++];
        }
        sortedIndex = right; 
    }

    private void quickSort(int[] array, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(array, low, high);
            quickSort(array, low, pivotIndex - 1);
            quickSort(array, pivotIndex + 1, high);
        }
    }

    private int partition(int[] array, int low, int high) {
        int pivot = array[high];
        pivotIndex = high; 
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (isPaused) {
                while (isPaused) {
                    try {
                        Thread.sleep(100); 
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return -1;
                    }
                }
            }
            if (array[j] < pivot) {
                i++;
                swap(array, i, j);
                activeIndex = j; 
                updateFeedback("Quick Sort: Swapping elements: " + array[i] + " and " + array[j]);
                quickSortPanel.repaint();
                sleep(500);
            }
        }
        swap(array, i + 1, high);
        pivotIndex = i + 1; 
        updateFeedback("Quick Sort: Pivot placed: " + array[i + 1]);
        quickSortPanel.repaint();
        sleep(500); 
        sortedIndex = i + 1; 
        return i + 1;
    }

    private void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    private void updateFeedback(String message) {
        SwingUtilities.invokeLater(() -> {
            feedbackArea.append(message + "\n");
        });
    }

    private void sleep(int millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        new SortingHeapAndMergeUi();
    }
}
