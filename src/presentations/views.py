from django.shortcuts import render, get_object_or_404

from .models import Presentation, Grade

# Create your views here.

def evaluation_form_page(request, evaluation_id, group_id, *args):

    presentation: Presentation = get_object_or_404(Presentation, evaluation_id=evaluation_id, group_id=group_id)

    presentators = presentation.presentators.all()

    evaluation: Evaluation = presentation.evaluation

    all_evaluations = evaluation.course.evaluation_set.all()
    all_presentations = []

    for other_evaluation in all_evaluations:
        for other_presentation in other_evaluation.presentation_set.all():
            all_presentations.append(other_presentation)

    allowed_evaluators_set = presentation.allowed_evaluators.all()

    group_members = presentation.group.student_set.all()

    grades = presentation.grade_set.all()

    all_grades = Grade.objects.filter(presentation__evaluation__course=evaluation.course)

    # Constructs the allowed evaluators' info, including their evaluation status
    allowed_evaluators = []

    for evaluator in allowed_evaluators_set:

        evaluator_answered_grades = 0
        evaluator_total_grades = 0

        for presentator in presentators:

            evaluator_answered_grades += grades.filter(state=True, evaluator=evaluator, presentation=presentation, student=presentator).count()

            evaluator_total_grades += grades.filter(evaluator=evaluator, presentation=presentation, student=presentator).count()

        evaluator_expected_grades = presentators.all().count()

        if evaluator_total_grades != evaluator_expected_grades:
            evaluator_status = "pending"
        elif evaluator_answered_grades != evaluator_expected_grades:
            evaluator_status = "evaluating"
        else:
            evaluator_status = "done"

        allowed_evaluators.append((evaluator.username, evaluator_status))

    # Constructs the group members' info, including their presentation statuses
    group_member_statuses = []

    for group_member in group_members:
        
        group_member_status = "pending"

        for other_presentation in all_presentations:
            print(all_grades.filter(presentation=other_presentation, student=group_member, state=True).count() == other_presentation.allowed_evaluators.all().count())
            print(all_grades.filter(presentation=other_presentation, student=group_member, state=True).count())
            print(other_presentation.allowed_evaluators.all().count())
            if ((other_presentation.presentators.filter(name=group_member.name, rut=group_member.rut).count() != 0) and 
                (all_grades.filter(presentation=other_presentation, student=group_member, state=True).count() == other_presentation.allowed_evaluators.all().count())):
                group_member_status = "done"
                break

        group_member_statuses.append((group_member.name, group_member_status))

    current_presentators = []

    for presentator in presentators:

        current_presentators.append(presentator.name)

    context = {
        "allowed_evaluators": allowed_evaluators,
        "group_members": group_member_statuses,
        "current_presentators": current_presentators,
    }

    return render(request, "evaluation_form.html", context);
