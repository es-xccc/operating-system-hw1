#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#define BUFFER_SIZE 4

int buffer[BUFFER_SIZE];
int count = 0;
int insert_index = 0;
int remove_index = 0;

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

void print_buffer() {
    printf("Buffer: [");
    for (int i = 0; i < count; i++) {
        printf("%d ", buffer[(remove_index + i) % BUFFER_SIZE]);
    }
    printf("]");
    printf("\n\n");
}

void* producer(void* arg) {
    int id = *((int*)arg);
    srand(time(NULL));
    for (int i = 1; i < 11; i++) {
        pthread_mutex_lock(&mutex);
        while (count == BUFFER_SIZE) {
            pthread_cond_wait(&cond, &mutex);
        }
        buffer[insert_index] = i;
        printf("Producer %d produced %d\n", id, i);
        insert_index = (insert_index + 1) % BUFFER_SIZE;
        count++;
        print_buffer();
        pthread_cond_signal(&cond);
        pthread_mutex_unlock(&mutex);
        usleep(rand() % 1000000);  // sleep for a random time between 0 and 1 second
    }
    printf("*****Producer %d finished.*****\n", id);
    return NULL;
}

void* consumer(void* arg) {
    int id = *((int*)arg);
    srand(time(NULL));
    for (int i = 1; i < 11; i++) {
        pthread_mutex_lock(&mutex);
        while (count == 0) {
            pthread_cond_wait(&cond, &mutex);
        }
        int item = buffer[remove_index];
        printf("Consumer %d consumed %d\n", id, item);
        remove_index = (remove_index + 1) % BUFFER_SIZE;
        count--;
        print_buffer();
        pthread_cond_signal(&cond);
        pthread_mutex_unlock(&mutex);
        usleep(rand() % 1000000 * 2);  // sleep for a random time between 0 and 1 second
    }
    printf("*****Consumer %d finished.*****\n", id);
    return NULL;
}

int main() {
    pthread_t producer_thread1, producer_thread2, consumer_thread1, consumer_thread2;
    int producer_id1 = 1, producer_id2 = 2, consumer_id1 = 1, consumer_id2 = 2;

    pthread_create(&producer_thread1, NULL, producer, &producer_id1);
    pthread_create(&producer_thread2, NULL, producer, &producer_id2);
    pthread_create(&consumer_thread1, NULL, consumer, &consumer_id1);
    pthread_create(&consumer_thread2, NULL, consumer, &consumer_id2);

    pthread_join(producer_thread1, NULL);
    pthread_join(producer_thread2, NULL);
    pthread_join(consumer_thread1, NULL);
    pthread_join(consumer_thread2, NULL);

    printf("All done.\n");

    return 0;
}