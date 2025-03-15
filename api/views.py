from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer, TeamSerializer, UserSerializer, StaticQuestionsSerializer
from .models import CompetitionTeams, AppUser, StaticQuestion, StaticReport, StaticAnswer
from rest_framework.exceptions import NotFound
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'statics': user.statics,
                'dynamics': user.dynamics,
                'scrutineering': user.scrutineering,
                'bpp': user.bpp,
                'cm': user.cm,
                'ed': user.ed
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'statics': user.statics,
                'dynamics': user.dynamics,
                'scrutineering': user.scrutineering,
                'bpp': user.bpp,
                'cm': user.cm,
                'ed': user.ed

            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        user = AppUser.objects.filter(id=pk).first()
        if user:
            return user

        raise NotFound({"detail": "No Movies matches the given query."})


class TeamsView(generics.ListAPIView):
    serializer_class = TeamSerializer

    def get_queryset(self):
        return CompetitionTeams.objects.filter(competition_id=1).prefetch_related('team')


class StaticBppQuestionsView(generics.ListAPIView):
    serializer_class = StaticQuestionsSerializer

    def get_queryset(self):
        return StaticQuestion.objects.filter(category='BPP')


class StaticEdQuestionsView(generics.ListAPIView):
    serializer_class = StaticQuestionsSerializer

    def get_queryset(self):
        return StaticQuestion.objects.filter(category='ED')


class TeamReportView(APIView):

    def get(self, request, pk, team_pk):
        # Get the user and team objects
        user = get_object_or_404(AppUser, pk=pk)
        team = get_object_or_404(CompetitionTeams, pk=team_pk)

        report = StaticReport.objects.filter(user=user, team=team).first()

        if report:
            return JsonResponse({
                'id': report.id,
                'team_id': report.team.id,
                'user_id': report.user.id,
                'notes': report.notes,
                'presenter': report.presenter
            })
        else:
            return JsonResponse({'message': 'Report not found'}, status=404)
    #### body {
    ####     "notes": "Some important notes",
    ####     "presenter": "John Doe"
    #### }
    def post(self, request, pk, team_pk):
        # Get the user and team objects
        user = get_object_or_404(AppUser, pk=pk)
        team = get_object_or_404(CompetitionTeams, pk=team_pk)

        # Check if the report already exists
        report = StaticReport.objects.filter(user=user, team=team).first()

        if report:
            # Update the existing report with the new data
            data = json.loads(request.body)
            report.notes = data.get('notes', report.notes)
            report.presenter = data.get('presenter', report.presenter)
            report.save()

            return JsonResponse({
                'id': report.id,
                'team_id': report.team.id,
                'user_id': report.user.id,
                'notes': report.notes,
                'presenter': report.presenter
            })
        else:
            # Create a new report if one doesn't exist
            data = json.loads(request.body)
            report = StaticReport.objects.create(
                user=user,
                team=team,
                notes=data.get('notes', ''),
                presenter=data.get('presenter', '')
            )

            return JsonResponse({
                'id': report.id,
                'team_id': report.team.id,
                'user_id': report.user.id,
                'notes': report.notes,
                'presenter': report.presenter
            }, status=201)


class TeamAnswersView(APIView):
    def get(self, request, pk, team_pk):
        # Get the user and team objects
        user = get_object_or_404(AppUser, pk=pk)
        team = get_object_or_404(CompetitionTeams, pk=team_pk)

        # Dohvati sve odgovore za odabrani tim i korisnika
        answers = StaticAnswer.objects.filter(team=team, user=user)

        answer_data = []
        for answer in answers:
            answer_data.append({
                'id': answer.id,
                'question_id': answer.question_id,
                'score': answer.score,
            })

        return JsonResponse({'answers': answer_data})

    # Ažuriranje odgovora za korisnika i tim
    #
    # {
    #     "answers": [
    #         {
    #             "question_id": 1,
    #             "score": 8,
    #             "answer_text": "Ovdje je moj odgovor na pitanje 1",
    #             "status": "approved"
    #         },
    #         {
    #             "question_id": 2,
    #             "score": 5,
    #             "answer_text": "Ovdje je moj odgovor na pitanje 2",
    #             "status": "pending"
    #         }
    #     ]
    # }
    def post(self, request, team_pk, user_pk):
        data = json.loads(request.body)
        team = get_object_or_404(CompetitionTeams, pk=team_pk)
        user = get_object_or_404(AppUser, pk=user_pk)

        # Loop through the submitted answers and update them
        for answer_data in data.get('answers', []):
            # question = get_object_or_404(StaticQuestion, pk=answer_data['question_id'])

            # Find the existing answer or create a new one
            answer, created = StaticAnswer.objects.update_or_create(
                team=team,
                user=user,
                question_id=answer_data['question_id'],
                defaults={
                    'score': answer_data.get('score', 0),
                }
            )

        return JsonResponse({'message': 'Answers updated successfully'}, status=200)
