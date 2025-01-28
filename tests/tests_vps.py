from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import VPS
import uuid


class VPSTests(APITestCase):

    def setUp(self):
        # Создаем тестовые VPS
        self.vps1 = VPS.objects.create(cpu=2, ram=4, hdd=100, status='started')
        self.vps2 = VPS.objects.create(cpu=4, ram=8, hdd=200, status='blocked')
        self.vps3 = VPS.objects.create(cpu=8, ram=16, hdd=500, status='stopped')


    def test_create_vps(self):
        """Тест создания нового VPS."""
        url = reverse('vps-list')
        data = {"cpu": 2, "ram": 8, "hdd": 200, "status": "started"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VPS.objects.count(), 4)
        self.assertEqual(response.data["cpu"], data["cpu"])
        self.assertEqual(response.data["ram"], data["ram"])
        self.assertEqual(response.data["hdd"], data["hdd"])
        self.assertEqual(response.data["status"], data["status"])

    def test_get_vps_list(self):
        """Тест получения списка всех VPS."""
        url = reverse('vps-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 3)


    def test_get_vps_detail(self):
        """Тест получения детальной информации по UID."""
        url = reverse('vps-detail', kwargs={'pk': str(self.vps1.uid)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["uid"]), str(self.vps1.uid))
        self.assertEqual(response.data["cpu"], self.vps1.cpu)
        self.assertEqual(response.data["ram"], self.vps1.ram)
        self.assertEqual(response.data["hdd"], self.vps1.hdd)
        self.assertEqual(response.data["status"], self.vps1.status)

    def test_get_vps_detail_not_found(self):
      """Тест получения детальной информации с несуществующим UID."""
      url = reverse('vps-detail', kwargs={'pk': str(uuid.uuid4())})
      response = self.client.get(url)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_vps(self):
        """Тест обновления VPS по UID."""
        url = reverse('vps-detail', kwargs={'pk': str(self.vps1.uid)})
        data = {"cpu": 4, "ram": 8, "hdd": 200, "status": "blocked"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vps1.refresh_from_db()
        self.assertEqual(self.vps1.cpu, data["cpu"])
        self.assertEqual(self.vps1.ram, data["ram"])
        self.assertEqual(self.vps1.hdd, data["hdd"])
        self.assertEqual(self.vps1.status, data["status"])


    def test_delete_vps(self):
      """Тест удаления VPS по UID"""
      url = reverse('vps-detail', kwargs={'pk': str(self.vps1.uid)})
      response = self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      self.assertEqual(VPS.objects.count(), 2)


    def test_change_status(self):
      """Тест изменения статуса VPS."""
      url = reverse('vps-change-status', kwargs={'pk': str(self.vps1.uid)})
      data = {'status': 'blocked'}
      response = self.client.post(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.vps1.refresh_from_db()
      self.assertEqual(self.vps1.status, 'blocked')


    def test_change_status_invalid_status(self):
        """Тест изменения статуса VPS с неверным статусом."""
        url = reverse('vps-change-status', kwargs={'pk': str(self.vps1.uid)})
        data = {'status': 'invalid_status'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_by_uid(self):
      """Тест фильтрации по uid."""
      url = reverse('vps-list') + f'?search={self.vps1.uid}'
      response = self.client.get(url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data.get('results')), 1)
      self.assertEqual(response.data.get('results')[0]['uid'], str(self.vps1.uid))


    def test_search_by_status(self):
      """Тест фильтрации по статусу."""
      url = reverse('vps-list') + f'?search=blocked'
      response = self.client.get(url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data.get('results')), 1)
      self.assertEqual(response.data.get('results')[0]['status'], 'blocked')

    def test_ordering_by_cpu(self):
       """Тест сортировки по cpu."""
       url = reverse('vps-list') + f'?ordering=cpu'
       response = self.client.get(url)
       self.assertEqual(response.status_code, status.HTTP_200_OK)
       self.assertEqual(len(response.data.get('results')), 3)
       self.assertEqual(response.data.get('results')[0]['cpu'], 2)
       self.assertEqual(response.data.get('results')[1]['cpu'], 4)
       self.assertEqual(response.data.get('results')[2]['cpu'], 8)


    def test_ordering_by_ram_desc(self):
       """Тест сортировки по ram в обратном порядке."""
       url = reverse('vps-list') + f'?ordering=-ram'
       response = self.client.get(url)
       self.assertEqual(response.status_code, status.HTTP_200_OK)
       self.assertEqual(len(response.data.get('results')), 3)
       self.assertEqual(response.data.get('results')[0]['ram'], 16)
       self.assertEqual(response.data.get('results')[1]['ram'], 8)
       self.assertEqual(response.data.get('results')[2]['ram'], 4)