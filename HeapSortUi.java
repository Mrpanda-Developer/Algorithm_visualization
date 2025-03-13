import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class HeapSortUI extends JFrame {

    private int[] array;
    private JPanel drawPanel;
    private JButton startButton;
    private boolean isSorting = false;
    private int sortedIndex = -1;
    private int currentIndex = -1;

    public HeapSortUI() {
        setTitle("Heap Sort Visualization");
        setSize(1200, 800);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        initializeArray();

        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());

        JLabel label = new JLabel("Heap Sort Visualization", SwingConstants.CENTER);

        startButton = new JButton("Start Sorting");

        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (!isSorting) {
                    isSorting = true;
                    startButton.setEnabled(false);
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            performHeapSort();
                            isSorting = false;
                            startButton.setEnabled(true);
                        }
                    }).start();
                }
            }
        });

        drawPanel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                drawArray(g);
                drawTree(g, getWidth() / 2, 50, 0, 300);
            }
        };
        drawPanel.setPreferredSize(new Dimension(1200, 700));

        panel.add(label, BorderLayout.NORTH);
        panel.add(startButton, BorderLayout.SOUTH);
        panel.add(drawPanel, BorderLayout.CENTER);

        add(panel);

        setVisible(true);
    }

    private void initializeArray() {
        array = new int[15];
        array[0] = 4;
        array[1] = 10;
        array[2] = 3;
        array[3] = 5;
        array[4] = 100;
        array[5] = 65;
        array[6] = 29;
        array[7] = 6;
        array[8] = 9;
        array[9] = 2;
        array[10] = 1;
        array[11] = 86;
        array[12] = 87;
        array[13] = 14;
        array[14] = 15;
    }

    private void drawArray(Graphics g) {
        int barWidth = getWidth() / array.length;
        for (int i = 0; i < array.length; i++) {
            int barHeight = array[i];

            if (i > sortedIndex) {
                g.setColor(Color.YELLOW);
            } else {
                g.setColor(Color.GREEN);
            }

            if (i == currentIndex) {
                g.setColor(Color.RED);
            }

            g.fillRect(i * barWidth, getHeight() - barHeight - 50, barWidth, barHeight);
            g.setColor(Color.BLACK);
            g.drawRect(i * barWidth, getHeight() - barHeight - 50, barWidth, barHeight);
        }
    }

    private void drawTree(Graphics g, int x, int y, int index, int xOffset) {
        if (index >= array.length) return;

        if (index > sortedIndex) {
            g.setColor(Color.YELLOW);
        } else {
            g.setColor(Color.GREEN);
        }

        if (index == currentIndex) {
            g.setColor(Color.RED);
        }

        g.fillOval(x - 40, y - 40, 80, 80);
        g.setColor(Color.BLACK);
        String number = Integer.toString(array[index]);
        FontMetrics fm = g.getFontMetrics();
        int textWidth = fm.stringWidth(number);
        int textHeight = fm.getAscent();
        int textX = x - textWidth / 2;
        int textY = y + textHeight / 2;
        g.drawString(number, textX, textY);

        int leftChild = 2 * index + 1;
        int rightChild = 2 * index + 2;

        if (leftChild < array.length) {
            int leftX = x - xOffset;
            int leftY = y + 100;
            g.setColor(Color.BLACK);
            g.drawLine(x, y + 40, leftX, leftY - 40);
            drawTree(g, leftX, leftY, leftChild, xOffset / 2);
        }

        if (rightChild < array.length) {
            int rightX = x + xOffset;
            int rightY = y + 100;
            g.setColor(Color.BLACK);
            g.drawLine(x, y + 40, rightX, rightY - 40);
            drawTree(g, rightX, rightY, rightChild, xOffset / 2);
        }
    }

    public void performHeapSort() {
        for (int i = array.length / 2 - 1; i >= 0; i--) {
            heapify(array.length, i);
        }

        for (int i = array.length - 1; i > 0; i--) {
            int temp = array[0];
            array[0] = array[i];
            array[i] = temp;

            sortedIndex = i;

            heapify(i, 0);

            repaint();
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private void heapify(int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n && array[left] > array[largest]) {
            largest = left;
        }

        if (right < n && array[right] > array[largest]) {
            largest = right;
        }

        if (largest != i) {
            int swap = array[i];
            array[i] = array[largest];
            array[largest] = swap;

            currentIndex = largest;

            repaint();
            try {
                Thread.sleep(3000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            heapify(n, largest);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new HeapSortUI();
           